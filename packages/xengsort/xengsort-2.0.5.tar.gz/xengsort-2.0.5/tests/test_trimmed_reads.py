from xengsort.io.fastqio import fastq_chunks_paired
from xengsort.io.generalio import InputFileHandler

def test_fastq_chunks_paired_file2_trimmed():
    with InputFileHandler("tests/data/test_chunks1.fq") as in1, \
         InputFileHandler("tests/data/test_chunks2.fq") as in2:
        pair = (in1, in2)
        reads1 = 0
        reads2 = 0
        for buf1, linemarks1, buf2, linemarks2 in fastq_chunks_paired(pair, bufsize=4000, maxreads=40):
            assert len(linemarks1) == len(linemarks2)
            for read in range(len(linemarks1)):
                for nuc in range(linemarks2[read][1]-linemarks2[read][0]-1):
                    assert buf2[linemarks2[read][0]:linemarks2[read][1]][nuc] == buf1[linemarks1[read][0]:linemarks1[read][1]][nuc]
            reads1 += len(linemarks1)
            reads2 += len(linemarks2)
            assert reads1 == reads2
        assert reads1 == 60

def test_fastq_chunks_paired_file1_trimmed():
    with InputFileHandler("tests/data/test_chunks2.fq") as in1, \
         InputFileHandler("tests/data/test_chunks1.fq") as in2:
        pair = (in1, in2)
        reads1 = 0
        reads2 = 0
        for buf1, linemarks1, buf2, linemarks2 in fastq_chunks_paired(pair, bufsize=4000, maxreads=40):
            assert len(linemarks1) == len(linemarks2)
            for read in range(len(linemarks1)):
                for nuc in range(linemarks1[read][1]-linemarks1[read][0]-1):
                    assert buf2[linemarks2[read][0]:linemarks2[read][1]][nuc] == buf1[linemarks1[read][0]:linemarks1[read][1]][nuc]
            reads1 += len(linemarks1)
            reads2 += len(linemarks2)
        assert reads1 == reads2 == 60
