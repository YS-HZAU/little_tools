import sys
import argparse
import itertools
import warnings
import traceback
import os.path

import HTSeq

class UnknownChrom(Exception):
    pass

def write_to_samout(r, assignment, samoutfile):
    if samoutfile is None:
        return
    if not pe_mode:
        r = (r,)
    for read in r:
        if read is not None:
            read.optional_fields.append(('XF', assignment))
            samoutfile.write(read.get_sam_line() + "\n")

def invert_strand(iv):
    iv2 = iv.copy()
    if iv2.strand == "+":
        iv2.strand = "-"
    elif iv2.strand == "-":
        iv2.strand = "+"
    else:
        raise ValueError("Illegal strand")
    return iv2


# CIGAR match characters (including alignment match, sequence match, and
# sequence mismatch
com = ('M', '=', 'X')

# sam_filenames,
insamfile = "test.sam"
# insamfile = "../allrich-09.RNA.bam"
# gff_filename,
gff_filename = "test.gtf"
# gff_filename = "MH63.gff3"
# samtype,
order = "pos"
# max_buffer_size
# stranded [yes reverse no]
# stranded -------------------------- 设计
# overlap_mode
overlap_mode = "intersection-nonempty"
# multimapped_mode  nonunique,
multimapped_mode = "none"
# secondary_alignment_mode, secondary_alignments 
secondary_alignment_mode = "ignore"
supplementary_alignment_mode = "ignore"
# feature_type  [gene  exon]
# id_attribute,
id_attribute = "ID" # gene_id transcript_id
# additional_attributes,
additional_attributes = []
minaqual = 10 
# samouts
outsamfile = "test.out.sam"
# outsamfile = "allrich-09.RNA.test.out.sam"
pe_mode = False

features_gene_strand = HTSeq.GenomicArrayOfSets("auto", True)
features_exon_strand = HTSeq.GenomicArrayOfSets("auto", True)
features_gene = HTSeq.GenomicArrayOfSets("auto", False)
features_exon = HTSeq.GenomicArrayOfSets("auto", False)
features_antisense = HTSeq.GenomicArrayOfSets("auto", True)
features_antisense_exon = HTSeq.GenomicArrayOfSets("auto", True)

counts_gene_strand = {}
attributes_gene_strand = {}
counts_exon_strand = {}
attributes_exon_strand = {}
counts_gene = {}
attributes_gene = {}
counts_exon = {}
attributes_exon = {}
counts_antisense = {}
attributes_antisense = {}
counts_antisense_exon = {}
attributes_antisense_exon = {}
i = 0

gff = HTSeq.GFF_Reader(gff_filename)
for f in gff:
    if f.type == "gene": # 存储基因track的
        feature_id = f.attr[id_attribute]  # 提取基因sense
        features_gene_strand[f.iv] += feature_id
        counts_gene_strand[f.attr[id_attribute]] = 0
        attributes_gene_strand[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes] # 将 gene name 或者其它属性绑定到 gene_id 上
        features_gene[f.iv] += feature_id  # 提取基因no sense
        counts_gene[f.attr[id_attribute]] = 0
        attributes_gene[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes] # 将 gene name 或者其它属性绑定到 gene_id 上

        tmp_iv = f.iv.copy()
        if tmp_iv.strand == "+":
            if tmp_iv.start < 250:
                tmp_iv.start = 0
            else:
                tmp_iv.start -= 250
        else:
            tmp_iv.end += 250
        features_antisense[tmp_iv] += feature_id
        counts_antisense[f.attr[id_attribute]] = 0
        attributes_antisense[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes]

        tmp_iv = f.iv.copy()
        if tmp_iv.strand == "+":
            tmp_pos = tmp_iv.start
            if tmp_iv.start < 250:
                tmp_iv.start = 0
            else:
                tmp_iv.start -= 250
            tmp_iv.end = tmp_pos
        else:
            tmp_pos = tmp_iv.end
            tmp_iv.end += 250
            tmp_iv.start = tmp_pos
        features_antisense_exon[tmp_iv] += feature_id
        counts_antisense_exon[f.attr[id_attribute]] = 0
        attributes_antisense_exon[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes]

    if f.type == "exon": # 存储exon
        feature_id = f.attr[id_attribute]
        features_exon_strand[f.iv] += feature_id
        counts_exon_strand[f.attr[id_attribute]] = 0
        attributes_exon_strand[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes]
        features_exon[f.iv] += feature_id
        counts_exon[f.attr[id_attribute]] = 0
        attributes_exon[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes]

        features_antisense_exon[f.iv] += feature_id
        counts_antisense_exon[f.attr[id_attribute]] = 0
        attributes_antisense_exon[f.attr[id_attribute]] = [f.attr[attr] if attr in f.attr else '' for attr in additional_attributes]

    i += 1
    if i % 100000 == 0:
        sys.stderr.write("%d GFF lines processed.\n" % i)
        sys.stderr.flush()
# read_iv = HTSeq.GenomicInterval( "chr1", 3073252,3074322, "+")
# sorted(set.union(*[val for iv, val in features_exon_strand[ read_iv ].steps()]))      overlap
# sorted(set.union(*[val for iv, val in features_exon[ read_iv ].steps()]))             overlap
# read_iv = HTSeq.GenomicInterval( "chr1", 3073252,3074322, "-")
# sorted(set.union(*[val for iv, val in features_exon_strand[ read_iv ].steps()]))      non-overlap
# sorted(set.union(*[val for iv, val in features_exon[ read_iv ].steps()]))             overlap
if len(counts_gene) == 0:
    sys.stderr.write("Warning: No features of type found.\n")


samoutfile = open(outsamfile, 'w')
if insamfile.endswith(".sam"):
    read_seq_file = HTSeq.SAM_Reader(insamfile)
else:
    read_seq_file = HTSeq.BAM_Reader(insamfile)
read_seq = iter(read_seq_file)

counts_all = []
empty_all = []
ambiguous_all = []
notaligned_all = []
lowqual_all = []
nonunique_all = []
empty_gene_strand = 0
ambiguous_gene_strand = 0
notaligned_gene_strand = 0
lowqual_gene_strand = 0
nonunique_gene_strand = 0
empty_exon_strand = 0
ambiguous_exon_strand = 0
notaligned_exon_strand = 0
lowqual_exon_strand = 0
nonunique_exon_strand = 0
empty_gene = 0
ambiguous_gene = 0
notaligned_gene = 0
lowqual_gene = 0
nonunique_gene = 0
empty_exon = 0
ambiguous_exon = 0
notaligned_exon = 0
lowqual_exon = 0
nonunique_exon = 0
empty_gene_reverse = 0
ambiguous_gene_reverse = 0
notaligned_gene_reverse = 0
lowqual_gene_reverse = 0
nonunique_gene_reverse = 0
empty_exon_reverse = 0
ambiguous_exon_reverse = 0
notaligned_exon_reverse = 0
lowqual_exon_reverse = 0
nonunique_exon_reverse = 0
i = 0

for r in read_seq:
    if i > 0 and i % 100000 == 0:
        sys.stderr.write("%d SAM alignment record%s processed.\n" % (i, "s" if not pe_mode else " pairs"))
        sys.stderr.flush()

    i += 1
    if not r.aligned:
        notaligned_gene_strand += 1
        notaligned_exon_strand +=1
        notaligned_gene +=1 
        notaligned_exon +=1 
        notaligned_gene_reverse +=1 
        notaligned_exon_reverse +=1
        r.optional_fields.append(('FG', "__not_aligned"))
        r.optional_fields.append(('FE', "__not_aligned"))
        r.optional_fields.append(('NG', "__not_aligned"))
        r.optional_fields.append(('NE', "__not_aligned"))
        r.optional_fields.append(('RG', "__not_aligned"))
        r.optional_fields.append(('RE', "__not_aligned"))
        samoutfile.write(r.get_sam_line() + "\n")
        continue
    if ((secondary_alignment_mode == 'ignore') and r.not_primary_alignment):
        continue
    if ((supplementary_alignment_mode == 'ignore') and r.supplementary):
        continue
    try:
        if r.optional_field("NH") > 1:
            nonunique_gene_strand +=1 
            nonunique_exon_strand +=1 
            nonunique_gene +=1 
            nonunique_exon +=1 
            nonunique_gene_reverse +=1 
            nonunique_exon_reverse +=1
            r.optional_fields.append(('FG', "__alignment_not_unique"))
            r.optional_fields.append(('FE', "__alignment_not_unique"))
            r.optional_fields.append(('NG', "__alignment_not_unique"))
            r.optional_fields.append(('NE', "__alignment_not_unique"))
            r.optional_fields.append(('RG', "__alignment_not_unique"))
            r.optional_fields.append(('RE', "__alignment_not_unique"))
            samoutfile.write(r.get_sam_line() + "\n")
            if multimapped_mode == 'none':
                continue
    except KeyError:
        pass
    if r.aQual < minaqual:
        lowqual_gene_strand +=1 
        lowqual_exon_strand +=1 
        lowqual_gene +=1 
        lowqual_exon +=1 
        lowqual_gene_reverse +=1 
        lowqual_exon_reverse +=1
        r.optional_fields.append(('FG', "__too_low_aQual"))
        r.optional_fields.append(('FE', "__too_low_aQual"))
        r.optional_fields.append(('NG', "__too_low_aQual"))
        r.optional_fields.append(('NE', "__too_low_aQual"))
        r.optional_fields.append(('RG', "__too_low_aQual"))
        r.optional_fields.append(('RE', "__too_low_aQual"))
        samoutfile.write(r.get_sam_line() + "\n")
        continue
    # iv_seq_yes = (co.ref_iv for co in r.cigar if co.type in com and co.size > 0)
    # iv_seq_reverse = (invert_strand(co.ref_iv) for co in r.cigar if (co.type in com and co.size > 0))
    
    try:
        fs = None
        iv_seq_yes = (co.ref_iv for co in r.cigar if co.type in com and co.size > 0)
        for iv in iv_seq_yes:
            if iv.chrom not in features_gene_strand.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_gene_strand[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('FG', "__no_feature"))
            empty_gene_strand +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('FG', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_gene_strand +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('FG', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_gene_strand[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_gene_strand[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")


        fs = None
        iv_seq_yes = (co.ref_iv for co in r.cigar if co.type in com and co.size > 0)
        for iv in iv_seq_yes:
            if iv.chrom not in features_exon_strand.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_exon_strand[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('FE', "__no_feature"))
            empty_exon_strand +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('FE', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_exon_strand +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('FE', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_exon_strand[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_exon_strand[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")


        fs = None
        iv_seq_yes = (co.ref_iv for co in r.cigar if co.type in com and co.size > 0)
        for iv in iv_seq_yes:
            if iv.chrom not in features_gene.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_gene[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('NG', "__no_feature"))
            empty_gene +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('NG', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_gene +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('NG', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_gene[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_gene[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")


        fs = None
        iv_seq_yes = (co.ref_iv for co in r.cigar if co.type in com and co.size > 0)
        for iv in iv_seq_yes:
            if iv.chrom not in features_exon.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_exon[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('NE', "__no_feature"))
            empty_exon +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('NE', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_exon +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('NE', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_exon[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_exon[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")

        
        
        fs = None
        iv_seq_reverse = (invert_strand(co.ref_iv) for co in r.cigar if (co.type in com and co.size > 0))
        for iv in iv_seq_reverse:
            if iv.chrom not in features_antisense.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_antisense[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('RG', "__no_feature"))
            empty_gene_reverse +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('RG', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_gene_reverse +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('RG', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_antisense[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_antisense[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")


        fs = None
        iv_seq_reverse = (invert_strand(co.ref_iv) for co in r.cigar if (co.type in com and co.size > 0))
        for iv in iv_seq_reverse:
            if iv.chrom not in features_antisense_exon.chrom_vectors:
                raise UnknownChrom
            for iv2, fs2 in features_antisense_exon[iv].steps():
                if (len(fs2) > 0):
                    if fs is None:
                        fs = fs2.copy()
                    else:
                        fs = fs.intersection(fs2)
        if fs is None or len(fs) == 0:
            # write_to_samout(r, "__no_feature", samoutfile)
            r.optional_fields.append(('RE', "__no_feature"))
            empty_exon_reverse +=1 
        elif len(fs) > 1:
            # write_to_samout(r, "__ambiguous[" + '+'.join(fs) + "]",samoutfile)
            r.optional_fields.append(('RE', "__ambiguous[" + '+'.join(fs) + "]"))
            ambiguous_exon_reverse +=1 
        else:
            # write_to_samout(r, list(fs)[0], samoutfile)
            r.optional_fields.append(('RE', list(fs)[0]))
        if fs is not None and len(fs) > 0:
            if multimapped_mode == 'none':
                if len(fs) == 1:
                    counts_antisense_exon[list(fs)[0]] += 1
            elif multimapped_mode == 'all':
                for fsi in list(fs):
                    counts_antisense_exon[fsi] += 1
            else:
                sys.exit("Illegal multimap mode.")
        samoutfile.write(r.get_sam_line() + "\n")


    except UnknownChrom:
        r.optional_fields.append(('FG', "__no_feature"))
        r.optional_fields.append(('FE', "__no_feature"))
        r.optional_fields.append(('NG', "__no_feature"))
        r.optional_fields.append(('NE', "__no_feature"))
        r.optional_fields.append(('RG', "__no_feature"))
        r.optional_fields.append(('RE', "__no_feature"))
        samoutfile.write(r.get_sam_line() + "\n")
        empty_gene_strand +=1 
        empty_exon_strand +=1 
        empty_gene +=1 
        empty_exon +=1 
        empty_gene_reverse +=1 
        empty_exon_reverse +=1 

sys.stderr.write("%d SAM %s processed.\n" % (i, "alignments " if not pe_mode else "alignment pairs"))
sys.stderr.flush()
samoutfile.close()

counts_all.append(counts_gene_strand.copy())
counts_all.append(counts_exon_strand.copy())
counts_all.append(counts_gene.copy())
counts_all.append(counts_exon.copy())
counts_all.append(counts_antisense.copy())
counts_all.append(counts_antisense_exon.copy())

empty_all.append(empty_gene_strand)
empty_all.append(empty_exon_strand)
empty_all.append(empty_gene)
empty_all.append(empty_exon)
empty_all.append(empty_gene_reverse)
empty_all.append(empty_exon_reverse)

ambiguous_all.append(ambiguous_gene_strand)
ambiguous_all.append(ambiguous_exon_strand)
ambiguous_all.append(ambiguous_gene)
ambiguous_all.append(ambiguous_exon)
ambiguous_all.append(ambiguous_gene_reverse)
ambiguous_all.append(ambiguous_exon_reverse)

lowqual_all.append(lowqual_gene_strand)
lowqual_all.append(lowqual_exon_strand)
lowqual_all.append(lowqual_gene)
lowqual_all.append(lowqual_exon)
lowqual_all.append(lowqual_gene_reverse)
lowqual_all.append(lowqual_exon_reverse)

notaligned_all.append(notaligned_gene_strand)
notaligned_all.append(notaligned_exon_strand)
notaligned_all.append(notaligned_gene)
notaligned_all.append(notaligned_exon)
notaligned_all.append(notaligned_gene_reverse)
notaligned_all.append(notaligned_exon_reverse)

nonunique_all.append(nonunique_gene_strand)
nonunique_all.append(nonunique_exon_strand)
nonunique_all.append(nonunique_gene)
nonunique_all.append(nonunique_exon)
nonunique_all.append(nonunique_gene_reverse)
nonunique_all.append(nonunique_exon_reverse)

for fn in sorted(counts_gene_strand.keys()):
    print('\t'.join([fn] + [str(c[fn]) for c in counts_all]))
print('\t'.join(["__no_feature"] + [str(c) for c in empty_all]))
print('\t'.join(["__ambiguous"] + [str(c) for c in ambiguous_all]))
print('\t'.join(["__too_low_aQual"] + [str(c) for c in lowqual_all]))
print('\t'.join(["__not_aligned"] + [str(c) for c in notaligned_all]))
print('\t'.join(["__alignment_not_unique"] + [str(c) for c in nonunique_all]))
