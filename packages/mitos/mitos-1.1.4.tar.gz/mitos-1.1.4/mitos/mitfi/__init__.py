'''
@author: M. Bernt
'''

import glob
import logging
import os
import re
from shutil import rmtree
from tempfile import mkdtemp

from mitos import util
from mitos.feature import mitfifeature  # ,feature
from mitos.trna import codon


class InfernalException(Exception):
    def __init__(self, command_line, exit_code, stderr):
        self.command_line = command_line
        self.exit_code = exit_code
        self.stderr = stderr

    def __str__(self):
        return "command: %s exit code %s stderr %s" % (self.command_line, self.exit_code, self.stderr)


def cmsearch(seqfile, outpath, code, gl=True, rRNA=None, trna=True, rrna=True, refdir=None):
    """
    run cmsearch (infernal) on one given file using available models in refdir

    @param[in] seqfile input file name
    @param[in] outpath output file name
    @param[in] code genetic code table to use for tRNA naming
    @param[in] gl if true then run cmsearch with option -g
    @param[in] rRNA list of rRNAs to check ("rrns"/"rrnL") run only the models
          for short/long rRNA otherwise all
        - if this option is set only the single models are run
        - rrna must be set to true
    @param[in] trna iff True run tRNA models
    @param[in] rrna iff True run rRNA models
    @param[in] refdir directory containing reference data
    """

    # determine set parameters for cmsearch and mitfi
    if gl:
        glopt = "g"
        cmsglob = ["-g"]
    else:
        glopt = "l"
        cmsglob = []

    # determine the models that should be run
    files = []

    if rRNA is not None:
        if "rrnS" in rRNA and os.path.exists("%s/modelle-v1/12smito-1.0.cm" % (refdir)):
            files.append("%s/modelle-v1/12smito-1.0.cm" % (refdir))
        if "rrnL" in rRNA and os.path.exists("%s/modelle-v1/16smito-1.0.cm" % (refdir)):
            files.append("%s/modelle-v1/16smito-1.0.cm" % (refdir))
    else:
        files += glob.glob("%s/modelle-v1/*-1.0.cm" % (refdir))

    # run cmsearch for each model and collect the -in parameters for mitfi
    rRNAinline = []
    tRNAinline = []
    for m in files:
        # logging.debug("cmsearch %s" % (m))
        ms = os.path.splitext(os.path.basename(m))[0]
        outfile = "%s%s.cmout" % (outpath, ms)
        if rrna and (ms.startswith("12smito") or ms.startswith("16smito")):
            rRNAinline += ["-in", outfile]
        elif trna and not (ms.startswith("12smito") or ms.startswith("16smito")):
            tRNAinline += ["-in", outfile]
        else:
            continue

        if os.path.exists(outfile):
            continue

#        print outfile
        cmd = ["cmsearch"] + cmsglob + ["--fil-no-hmm", "--fil-no-qdb", m, seqfile]
        out, err = util.execute(cmd, InfernalException)
        with open(outfile, "wb") as f:
            f.write(out)

    mitfipath = os.path.join(os.path.dirname(__file__), 'parser', 'mitfi_import.jar')
    mitfficodepath = os.path.join(os.path.dirname(__file__), 'parser', 'mitfiGeneticCodes')
    # run mitfi for tRNAs if
    # - trnas are to be predicted (and not only the rRNAs)
    # - mitfi output does not exist
    if (rRNA is None and trna > 0) and (not os.path.exists("%s/tRNAout.nc" % outpath)):
        cmd = ["java", "-jar", mitfipath, "-method", glopt, "-code", str(code), "-codefile", mitfficodepath, "-structure", "-genome", seqfile] + tRNAinline
        out, err = util.execute(cmd)
        with open(os.path.join(outpath, "tRNAout.nc"), "wb") as f:
            f.write(out)

    # run mitfi for rRNAs if
    # - rRNAs are to be predicted
    # - and mitfi output does not exist
    if (rRNA is not None or rrna > 0) and not os.path.exists("%s/rRNAout.nc" % outpath):
        cmd = ["java", "-jar", mitfipath, "-method", glopt, "-code", str(code), "-codefile", mitfficodepath, "-structure", "-ribosomal", "-genome", seqfile] + rRNAinline
        out, err = util.execute(cmd)
        with open(os.path.join(outpath, "rRNAout.nc"), "wb") as f:
            f.write(out)


def cmrealign(sequence, rRNA, refdir):
    """
    function to realign a subsequence to a model in order to get the structure.

    @param[in] sequence sequence to realign
    @param[in] rRNA type of rRNA to realign (rrnS/rrnL)
    @param[in] refdir directory containing reference data
    @return structure
    """
    tdir = mkdtemp()

    # write sequence to tmp file
    f = open(tdir + "/cmrealign.fas", "w")
    f.write("> rnasubsequence\n")
    f.write("%s\n" % str(sequence))
    f.close()

    if rRNA == "rrnS":
        model = "%s/modelle-v1/12smito-1.0.cm" % (refdir)
    elif rRNA == "rrnL":
        model = "%s/modelle-v1/16smito-1.0.cm" % (refdir)
    else:
        logging.error("cmrealign: unknown model %s" % rRNA)
        return

    # realign
    args = ["cmalign", "-1", "-o", "%s/cmrealign.stk" % (tdir), model, "%s/cmrealign.fas" % (tdir)]
    out, err = util.execute(args, InfernalException)
    with open("%s/cmrealign.out" % tdir, "wb") as f:
        f.write(out)

    mitfiimppath = os.path.join(os.path.dirname(__file__), 'parser', 'improve_infernal_structure.jar')

    # improve structure
    cmd = ["java", "-jar", mitfiimppath, f"{tdir}/cmrealign.stk"]
    util.execute(cmd)
    with open(f"{tdir}/cmrealign.stk", "wb") as f:
        f.write(out)

    # get structure
    with open(tdir + "/cmrealign.str") as f:
        structure = f.readlines()[2].strip()

    rmtree(tdir)

    return structure


def parse(inpath, local):
    """
    parse single mitfifile and returns list of features
    @parm inpath filehandler mitfifile
    @param local
    @return feature list
    """

    features = []
    files = glob.glob(inpath + "/*.nc")
    for resultfile in files:
        mitfihandle = open(resultfile)
        # counts in witch line is next
        # 1 = first line of feature (data)
        # 2 = sequence of feature
        # 3 = structure of feature
        linecounter = 0
        # read the 3. line
        line = mitfihandle.readline()
        while line != "":
            if linecounter % 3 == 0:
                cols = line[1:].split("|")
                # code = int(cols[1])                       #code
                start = int(cols[2]) - 1  # genom-start-position
                stop = int(cols[3]) - 1  # genom-ende-position
                strand = int(cols[4])  # strand
                qstart = int(cols[5]) - 1  # model-start-position(bei global immer 1)
                qstop = int(cols[6]) - 1  # model-ende-position
                # score = float(cols[7])                    #infernal-score
                evalue = float(cols[8])  # e-value
                pvalue = float(cols[9])  # p-value
                # gccontent = int(cols[10])                 #GC-content
                anticodonpos = int(cols[11]) - 1  # Anticodon-start-position
                if anticodonpos >= 0:  # Anticodon
                    anticodon = codon(cols[12], "anticodon")
                else:
                    anticodon = None
                    anticodonpos = None

                # TODO: this regex is a workaround to the new model names
                # which are not correctly treated by mitfi
                mt = re.match(r"(\w\d*)-\d\.\d", cols[13])
                if mt is not None:
                    name = mt.group(1)
                else:
                    name = cols[13]  # Aminosaeure

                model = cols[14]  # model
                tophit = int(cols[15])  # tophit=1
                kopie = int(cols[16])  # Kopie=1

                if cols[17].strip() == "g":  # g(lobal) oder l(okal)
                    local = 0
                else:
                    local = 1

                if tophit:
                    mito = 2
                elif kopie:
                    mito = 1
                else:
                    mito = 0

                if model.startswith("12smito"):
                    type = "rRNA"
                    name = "rrnS"
                    model = "rrnS"

                elif model.startswith("16smito"):
                    type = "rRNA"
                    name = "rrnL"
                    model = "rrnL"
                else:
                    type = "tRNA"
                    model = model[8:-7]
                    name = "trn%s" % (name)

            elif linecounter % 3 == 1:
                sequence = line.strip()
            else:  # linecounter % 3 ==2
                score = evalue
                structure = re.sub(r"[-]", ".", line.strip())
                features.append(
                    mitfifeature(
                        name=name, type=type, start=start, stop=stop,
                        strand=strand, method="mitfi", score=score,
                        sequence=sequence, struct=structure, anticodonpos=anticodonpos,
                        anticodon=anticodon, qstart=qstart,
                        qstop=qstop, evalue=evalue, pvalue=pvalue, model=model,
                        local=local, mito=mito
                    )
                )
            linecounter += 1

            line = mitfihandle.readline()
        mitfihandle.close()
    return features


def parse_feature(inpath, local, name, start, stop, strand):
    """
    get a certain feature from the mitfi file
    @param name name of the feature
    @param start start position of the feature
    @param stop stop position of the feature
    @param strand strand of the feature
    """

    # get the feature(s) matching the name, start, stop, and strand
    features = [x for x in parse(inpath, local) if
                (x.name == name and x.start == start and x.stop == stop and x.strand == x.strand)]

    if len(features) == 1:
        return features[0]
    elif len(features) == 0:
        logging.error("no feature %s %d %d %d found in %s" % (name, start, stop, strand, inpath))
        return None
    else:
        logging.error("more than one feature %s %d %d %d found in %s" % (name, start, stop, strand, inpath))
        return features[0]
