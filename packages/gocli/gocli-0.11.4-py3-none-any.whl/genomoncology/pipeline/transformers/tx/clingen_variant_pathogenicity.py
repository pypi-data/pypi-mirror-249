from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import (
    register,
    name_mapping,
    split_value,
)
import re

SPLIT_CHARS = ",;"

list_of_ncs = {
    "NC_000001.10",
    "NC_000002.11",
    "NC_000003.11",
    "NC_000004.11",
    "NC_000005.9",
    "NC_000006.11",
    "NC_000007.13",
    "NC_000008.10",
    "NC_000009.11",
    "NC_000010.10",
    "NC_000011.9",
    "NC_000012.11",
    "NC_000013.10",
    "NC_000014.8",
    "NC_000015.9",
    "NC_000016.9",
    "NC_000017.10",
    "NC_000018.9",
    "NC_000019.9",
    "NC_000020.10",
    "NC_000021.8",
    "NC_000022.10",
    "NC_000023.10",
    "NC_000024.9",
    "NC_012920.1",
}

NAME_MAPPING = {
    "hgvs_g": "HGVS Expressions",
    "clinvar_id__string": "ClinVar Variation Id",
    "gene": "HGNC Gene Symbol",
    "disease_string": "Disease",
    "mode_of_inheritance__string": "Mode of Inheritance",
    "significance__string": "Assertion",
    "evidence_codes__mstring": "Applied Evidence Codes (Met)",
    "interpretation_summary__string": "Summary of interpretation",
    "pubmed_ids__mstring": "PubMed Articles"
}


def get_correct_hgvs_g(x):
    list_of_hgvs_gs = x["hgvs_g"].split(', ')
    # get a list of all records beginning with NC_...
    list_of_nc_records = [ncrec for ncrec in list_of_hgvs_gs if ncrec.startswith("NC_")
                          and re.search('NC_[0-9]+.[0-9]+',
                                        ncrec).group() in list_of_ncs]

    # change the value of any NC_012920.1:m -> NC_012920.1:g
    list_of_nc_records = [re.sub("NC_012920.1:m", "NC_012920.1:g", rec) for rec in
                          list_of_nc_records]
    if len(list_of_nc_records) > 0:
        # use the nc record.
        return list_of_nc_records[0]
    else:
        # If there are no NC records then send the NM records without ()
        list_if_nm_records = [nmrec for nmrec in list_of_hgvs_gs if
                              nmrec.startswith("NM_") and "(" not in nmrec]
        if len(list_if_nm_records) > 0:
            return list_if_nm_records[0]
        else:
            return None


def split_values(x, key):
    value = x.get(key, [])
    return split_value(value, split_chars=SPLIT_CHARS) if value else []


register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_VARIANT_PATHOGENICITY,
    transformer=compose(
        lambda x: assoc(x, "hgvs_g", get_correct_hgvs_g(x)),
        lambda x: assoc(x, __TYPE__, DocType.CLINGEN_VARIANT_PATHOGENICITY.value),
        name_mapping(NAME_MAPPING, empty_values=(None, "", ".", [])),
    ),
)

register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_VARIANT_PATHOGENICITY,
    transformer=compose(
        lambda x: assoc(x, __CHILD__, DocType.CLINGEN_VARIANT_PATHOGENICITY.value),
    ),
    is_header=True,
)
