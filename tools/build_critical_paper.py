"""Build the research paper's TXT/PDF from its canonical Markdown.

Experiments need only the Python standard library. Document building separately
requires pandoc and reportlab==4.4.9, plus DejaVu fonts on the rendering host.
"""
from pathlib import Path
import argparse
import re
import subprocess
import tempfile
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
STEM='WHEN_THE_MAP_BECOMES_THE_AUTHORITY'
MIXED_STEM='MPLPB_MIXED_DUMP'
SWITCH_STEM='PROBABILISTIC_PROMPTS_AND_MPLPB_CONTRACTS'
PAPERS={'critical':STEM,'mixed-dump':MIXED_STEM,'switch-test':SWITCH_STEM,'testing-oocc':'TESTING_OOCC'}
METADATA={
    'TESTING_OOCC':('Testing OOCC',
                    'Claims, Required Tests, and a Roadmap to Verified Behavior',
                    'McPhetridge · Testing OOCC v1.3 · 20 November 2026 · Author-review draft'),
    STEM:('MPLPB and OOCC/CAD: Comparative Experiments',
          'Critical OOCC/CAD experiments and source-governance boundaries',
          'McPhetridge · Research draft · 16 November 2026'),
    MIXED_STEM:('MPLPB Mixed Dump',
                'Source-bounded review, proof admission, and mixed-document testing',
                'McPhetridge · MPLPB Mixed Dump · 18 November 2026'),
    SWITCH_STEM:('Probabilistic Prompts and MPLPB Deterministic Contracts',
                 'The 8 a.m. Switch Test for Instructions and Effects',
                 'McPhetridge · The Switch Test · 18 November 2026'),
}


def build(out, stem=STEM):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted
    source=ROOT/'docs/paper'/f'{stem}.md'
    title_text,subject,footer_text=METADATA[stem]
    out.mkdir(parents=True,exist_ok=True)
    # Preserve link destinations in TXT/PDF; pandoc plain otherwise drops them.
    def link_text(match):
        label,url=match.groups()
        if not url.startswith(('https://','http://','#')):
            target=(source.parent/url).resolve().relative_to(ROOT)
            url='https://github.com/mitchell-d00/B-Tests/blob/main/'+str(target)
        return label+' ('+url+')'
    printable=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link_text,source.read_text())
    plain=subprocess.run(['pandoc','-f','gfm','-t','plain','--wrap=auto','--columns=88'],input=printable,check=True,capture_output=True,text=True).stdout
    (out/f'{stem}.txt').write_text(plain)
    fontdir=Path('/usr/share/fonts/truetype/dejavu')
    for name,file in [('PaperSerif','DejaVuSerif.ttf'),('PaperSans','DejaVuSans.ttf'),('PaperSansBold','DejaVuSans-Bold.ttf'),('PaperMono','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
    body=ParagraphStyle('body',fontName='PaperSerif',fontSize=9.5,leading=13.1,spaceAfter=7,splitLongWords=True)
    heading=ParagraphStyle('heading',parent=body,fontName='PaperSansBold',fontSize=12,leading=15,spaceBefore=12,spaceAfter=8,keepWithNext=True)
    title=ParagraphStyle('title',parent=heading,fontSize=17,leading=21,alignment=TA_CENTER,spaceBefore=0,spaceAfter=10)
    code=ParagraphStyle('code',fontName='PaperMono',fontSize=7,leading=9,spaceAfter=8)
    headings={re.sub(r'^#+\s+','',l).strip() for l in source.read_text().splitlines() if l.startswith('#')}
    story=[]
    for block in re.split(r'\n\s*\n',plain.strip()):
        text=' '.join(block.splitlines()).strip()
        if not text:continue
        if text==source.read_text().splitlines()[0].removeprefix('# '):style=title
        elif text in headings:style=heading
        else:style=body
        if all(l.startswith('    ') for l in block.splitlines()):
            story.append(Preformatted(block,code,maxLineLength=105));continue
        story.append(Paragraph(escape(text),style))
    def footer(c,doc):
        c.saveState();c.setFont('PaperSans',7);c.setFillColor(colors.HexColor('#555555'))
        c.drawString(43,25,footer_text)
        c.drawRightString(A4[0]-43,25,str(doc.page));c.restoreState()
    def fixed_canvas(*args,**kwargs):kwargs['invariant']=1;return canvas.Canvas(*args,**kwargs)
    doc=SimpleDocTemplate(str(out/f'{stem}.pdf'),pagesize=A4,rightMargin=43,leftMargin=43,topMargin=42,bottomMargin=42,
        title=title_text,author='Mitchell D. McPhetridge',subject=subject)
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=fixed_canvas)
    return plain


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',action='store_true')
    p.add_argument('--paper',choices=PAPERS,default='critical')
    a=p.parse_args()
    stem=PAPERS[a.paper]
    destination=ROOT/'docs/paper'
    if a.check:
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);build(out,stem)
            for suffix in ('txt','pdf'):
                assert (out/f'{stem}.{suffix}').read_bytes()==(destination/f'{stem}.{suffix}').read_bytes(),suffix+' differs; rebuild or check document-tool/font versions'
        print('TXT and PDF match canonical Markdown under this renderer')
    else:
        build(destination,stem);print(destination)

if __name__=='__main__':main()
