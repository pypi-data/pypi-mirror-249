import argparse

from pysam import VariantFile


def read_vcf(filename, mod_func=None):
    with VariantFile(filename) as vcf_file:
        # Assume single sample VCF files for now (and forever)
        assert len(vcf_file.header.samples) == 1

        phase_sets = {}
        active_ps_id = 0
        for rec in vcf_file.fetch():
            entry = rec.samples[0]

            ps_id = entry.get("PS")
            if entry.phased:
                ps_id = ps_id or active_ps_id
            if not ps_id:
                ps_id = rec.pos
                active_ps_id = ps_id if entry.phased else 0

            key = rec.chrom, ps_id
            if key not in phase_sets:
                phase_sets[key] = [[] for _ in entry["GT"]]

            for idx, gt in enumerate(entry["GT"]):
                if gt:
                    alt = rec.alts[gt - 1]
                    if "<" in alt or ">" in alt:
                        raise ValueError("Cannot deal with symbolic alleles")

                    if alt == "*":
                        continue

                    if callable(mod_func):
                        variant = mod_func(rec.start, rec.stop, rec.ref, alt)
                    else:
                        variant = rec.start, rec.stop, rec.ref
                    phase_sets[key][idx].append(variant)

        return vcf_file.header.samples[0], {key: value for key, value in phase_sets.items() if any(value)}


def main():
    parser = argparse.ArgumentParser(description="Read phase sets from single sample VCF 4.3 file.")
    parser.add_argument("filename", help="VCF file")
    args = parser.parse_args()

    phase_sets = read_vcf(args.filename)
    for (chrom, ps), alleles in phase_sets.items():
        print(f"{chrom}:{ps}")
        for idx, allele in enumerate(alleles):
            print(f"\t{idx}: {allele}")



if __name__ == "__main__":
    main()
