import copy
from pathlib import Path
from typing import Tuple

import gffpandas.gffpandas as gffpd
import pandas as pd
import os
from Bio import SeqIO
from Bio.Seq import MutableSeq
from Bio.Seq import Seq
import re


class CandidateGeneAnalyzer:
    basePath: str
    sequenceData: dict
    mutationData: dict
    genomicAnnotations: pd.DataFrame
    genesOfInterest: pd.DataFrame
    pat = re.compile(r"ID=[^;]*")

    def set_genes_of_interest(self, path: os.path) -> None:
        genes = pd.DataFrame()
        for file in os.listdir(path):
            genes = pd.concat([genes, pd.read_csv(path + "/" + file, sep="\t")])
        self.genesOfInterest = genes

    def set_genomic_annotations(self, path: os.path) -> None:
        genomicAnnotations = pd.DataFrame()
        for file in os.listdir(path):
            genomicAnnotations = pd.concat(
                [
                    genomicAnnotations,
                    pd.read_csv(
                        path + "/" + file,
                        sep="\t",
                        comment="#",
                        names=[
                            "Chromosome",
                            "Source",
                            "Feature",
                            "Start",
                            "End",
                            "Unknown",
                            "Strand",
                            "Unknown2",
                            "Attributes",
                        ],
                    ),
                ]
            )
        genomicAnnotations["GeneInfo"] = genomicAnnotations["Attributes"].apply(
            lambda x: self.pat.search(x).group(0).split("=")[1]
        )
        self.genomicAnnotations = genomicAnnotations

    def set_sequence_data(self, path: os.path, set_mutation_data: bool) -> None:
        sequenceData = {}
        for file in os.listdir(path):
            sequenceData.update(SeqIO.to_dict(SeqIO.parse(path + "/" + file, "fasta")))
        self.sequenceData = sequenceData
        if set_mutation_data:
            self.set_mutation_data()

    def set_mutation_data(self) -> None:
        if self.sequenceData is None:
            raise Exception("Sequence data is not initialized!")
        mutations = copy.deepcopy(self.sequenceData)
        for series in self.genesOfInterest.iterrows():
            row = series[1]
            geneName = row["Chromosome"]
            mutationIndex = row["Position"] - 1
            newBase = row["Alt"]
            oldBase = row["Ref"]
            if self.sequenceData[geneName].seq[mutationIndex] != oldBase:
                raise Exception(
                    "Mutation at position "
                    + str(mutationIndex)
                    + " on Chromosome "
                    + geneName
                    + " does not match reference!"
                )
            mutableSequence = MutableSeq(str(mutations[geneName].seq))
            mutableSequence[mutationIndex] = newBase
            mutations[geneName].seq = Seq(mutableSequence)
        self.mutationData = mutations

    def get_sequence_df_for_chromosome(self, chromosome: str) -> pd.DataFrame:
        self.is_ready_to_find_candidate_genes()
        df = self.genesOfInterest
        locusNames = (
            df.loc[df["Chromosome"] == chromosome]["locusName"].unique().tolist()
        )
        filteredAnnotations = self.genomicAnnotations.loc[
            self.genomicAnnotations["GeneInfo"].str.contains(
                "|".join(locusNames), regex=True
            )
            & (self.genomicAnnotations["Feature"].str.contains("CDS"))
        ]
        sequence_df = filteredAnnotations[
            ["Chromosome", "Start", "End", "Strand", "GeneInfo"]
        ].copy()
        sequence_df["GeneID"] = sequence_df["GeneInfo"].apply(
            lambda x: ".".join(x.split(".")[0:2])
        )
        sequence_df["Version"] = sequence_df["GeneInfo"].apply(
            lambda x: x.split(".")[2]
        )
        sequence_df["GeneIndex"] = sequence_df["GeneInfo"].apply(
            lambda x: x.split(".")[-1]
        )
        sequence_df["Sequence"] = sequence_df.apply(
            lambda x: str(
                self.sequenceData[x["Chromosome"]].seq[x["Start"] - 1 : x["End"]]
            ),
            axis=1,
        )
        sequence_df["MutatedSequence"] = sequence_df.apply(
            lambda x: str(
                self.mutationData[x["Chromosome"]].seq[x["Start"] - 1 : x["End"]]
            ),
            axis=1,
        )
        return sequence_df

    def build_sequence_for_chromosome(self, chromosome: str) -> pd.DataFrame:
        self.is_ready_to_find_candidate_genes()
        sequence_df = self.get_sequence_df_for_chromosome(chromosome)
        forward_df = (
            sequence_df.loc[sequence_df["Strand"] == "+"]
            .sort_values(by=["GeneIndex"], ascending=True)
            .groupby(["GeneID", "Version"])[["Sequence", "MutatedSequence"]]
            .agg("".join)
            .reset_index()
        )
        reverse_df = (
            sequence_df.loc[sequence_df["Strand"] == "-"]
            .sort_values(by=["GeneIndex"], ascending=False)
            .groupby(["GeneID", "Version"])[["Sequence", "MutatedSequence"]]
            .agg("".join)
            .reset_index()
        )
        forward_df["Sequence"] = forward_df["Sequence"].apply(lambda x: Seq(x))
        forward_df["MutatedSequence"] = forward_df["MutatedSequence"].apply(
            lambda x: Seq(x)
        )
        reverse_df["Sequence"] = reverse_df["Sequence"].apply(
            lambda x: Seq(x).reverse_complement(inplace=False)
        )
        reverse_df["MutatedSequence"] = reverse_df["MutatedSequence"].apply(
            lambda x: Seq(x).reverse_complement(inplace=False)
        )
        df = pd.concat([forward_df, reverse_df])
        df["ProteinSequence"] = df["Sequence"].apply(lambda x: x.translate())
        df["MutatedProteinSequence"] = df["MutatedSequence"].apply(
            lambda x: x.translate()
        )
        return df

    def build_sequences_for_all_chromosomes(self) -> dict:
        self.is_ready_to_find_candidate_genes()
        sequences = {}
        for chromosome in self.genesOfInterest["Chromosome"].unique():
            sequences[chromosome] = self.build_sequence_for_chromosome(chromosome)
        return sequences

    def build_and_save_sequences_for_all_chromosomes(self, output_path: str) -> dict:
        self.is_ready_to_find_candidate_genes()
        sequences = self.build_sequences_for_all_chromosomes()
        df = pd.concat(sequences.values())
        df.to_csv(output_path, sep="\t", index=False)
        return sequences

    def is_ready_to_find_candidate_genes(self) -> None:
        if not (
            self.genomicAnnotations is not None
            and self.sequenceData is not None
            and self.mutationData is not None
            and self.genesOfInterest is not None
        ):
            raise Exception("Not all data is initialized!")


class PromotorExtraction:
    log_fold_change_border: float = -1.0
    promotor_upstream: int = 500
    promotor_downstream: int = 200
    p_adjusted_min: float = 0.01
    start_codon: str = "ATG"
    genes_of_interest_df: pd.DataFrame
    sequence_dict: dict
    annotation_df: pd.DataFrame

    def set_genes_of_interest(self, path: str) -> None:
        genes = pd.DataFrame()
        if Path(path).is_dir():
            for file in os.listdir(path):
                genes = pd.concat([genes, pd.read_csv(path + "/" + file, sep="\t")])
        else:
            genes = pd.read_csv(path, sep="\t")
        self.genes_of_interest_df = genes

    def set_sequence_df(self, path: str) -> None:
        sequenceData = {}
        if Path(path).is_dir():
            for file in os.listdir(path):
                sequenceData.update(
                    SeqIO.to_dict(SeqIO.parse(path + "/" + file, "fasta"))
                )
        else:
            sequenceData.update(SeqIO.to_dict(SeqIO.parse(path, "fasta")))
        self.sequence_dict = sequenceData

    def set_annotation_df(self, path: str) -> None:
        df = pd.DataFrame()
        if Path(path).is_dir():
            for file in os.listdir(path):
                annot = gffpd.read_gff3(path + "/" + file)
                annot_df = annot.attributes_to_columns()
                df = pd.concat(
                    [
                        df,
                        annot_df,
                    ]
                )
        else:
            annot = gffpd.read_gff3(path)
            df = annot.attributes_to_columns()
        df["start"] = df["start"].astype(int)
        df["end"] = df["end"].astype(int)
        df["start"] = df["start"].apply(lambda x: x - 1)
        df["end"] = df["end"].apply(lambda x: x - 1)
        df["Version"] = df["ID"].apply(lambda x: x.split(".")[2])
        df["GeneIndex"] = df["ID"].apply(lambda x: x.split(".")[-1])
        self.annotation_df = df

    def get_promotor_df(self, path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.is_ready_to_find_promotors()
        df = self.genes_of_interest_df
        annot_df = self.annotation_df.copy()
        annot_df = annot_df[annot_df["type"] == "CDS"]
        annot_df["GeneIndex"] = annot_df["GeneIndex"].astype(int)
        annot_df["Version"] = annot_df["Version"].astype(int)
        annot_df["Parent_cds"] = annot_df["Parent"].apply(
            lambda x: ".".join(x.split(".")[0:2] + x.split(".")[3:])
        )
        df = pd.merge(
            df,
            annot_df,
            left_on="GeneID",
            right_on="Parent_cds",
            how="left",
        )
        df = df[(df["GeneIndex"] == 1) & (df["Version"] == 1)]
        df = df[
            [
                "GeneID",
                "seq_id",
                "log2FoldChange",
                "padj",
                "start",
                "end",
                "strand",
                "Parent",
                "Parent_cds",
            ]
        ]
        upregulated_df: pd.DataFrame = df[
            (df["log2FoldChange"] <= self.log_fold_change_border)
            & (df["padj"] < self.p_adjusted_min)
        ].copy()
        downregulated_df: pd.DataFrame = df[
            (df["log2FoldChange"] >= self.log_fold_change_border)
            & (df["padj"] < self.p_adjusted_min)
        ].copy()
        upregulated_df[["Sequence", "ATG_Condition"]] = upregulated_df.apply(
            self.build_sequence, axis=1, result_type="expand"
        )
        downregulated_df[["Sequence", "ATG_Condition"]] = downregulated_df.apply(
            self.build_sequence, axis=1, result_type="expand"
        )
        if path is not None:
            upregulated_df.to_csv(path + "/Upregulated.tsv", sep="\t", index=False)
            downregulated_df.to_csv(path + "/Downregulated.tsv", sep="\t", index=False)
        return upregulated_df, downregulated_df

    def build_sequence(self, row: pd.Series) -> Tuple[str, bool]:
        if row["strand"] == "+":
            beginning = (
                row["start"] - self.promotor_upstream
                if row["start"] > self.promotor_upstream
                else 0
            )
            end = (
                row["start"] + self.promotor_downstream
                if len(self.sequence_dict[row["seq_id"]])
                >= row["start"] + self.promotor_downstream
                else len(self.sequence_dict[row["seq_id"]])
            )
            sequence = self.sequence_dict[row["seq_id"]][beginning:end]
            prom = sequence.seq[500:503]
            return str(sequence.seq), str(prom) == self.start_codon
        else:
            beginning = (
                row["end"] - self.promotor_downstream
                if row["end"] > self.promotor_downstream
                else 0
            )
            end = (
                row["end"] + self.promotor_upstream
                if len(self.sequence_dict[row["seq_id"]])
                >= row["end"] + self.promotor_upstream
                else len(self.sequence_dict[row["seq_id"]])
            )
            sequence = self.sequence_dict[row["seq_id"]][beginning:end]
            sequence = sequence.reverse_complement()
            prom = sequence.seq[499:502]
            return str(sequence.seq), str(prom) == self.start_codon

    def is_ready_to_find_promotors(self) -> None:
        if not (
            self.annotation_df is not None
            and self.sequence_dict is not None
            and self.genes_of_interest_df is not None
        ):
            raise Exception("Not all data is initialized!")
