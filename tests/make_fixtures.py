# 2026-11-24 실제 응답에서 잘라낸 샘플로 fixture 생성
import os
d = "fixtures"
rss_items = [
 ("[무신사] 내셔널지오그래픽 키즈 블레이즈 부츠 (59,040원/무배)", 751370, "사이즈가 240 까지 있어서 여성용으로도 괜찮을듯요", "Tue, 24 Nov 2026 06:15:19 GMT"),
 ("[롯데온] 스타벅스 캡슐커피 대용량 90캡슐+카푸치노 머그 2개 증정 (47,740원/무료)", 751369, "스벅 캡슐커피 하나에 530원정도네요", "Tue, 24 Nov 2026 06:05:58 GMT"),
 ("[G마켓] 올반 핫도그 30봉 (찰15+크런치15) (20,840원/무료)", 751368, "1개당 694원농협카드 결제면 1천원 할인", "Tue, 24 Nov 2026 06:03:17 GMT"),
]
x = '<?xml version="1.0" encoding="UTF-8" ?>\n<rss xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">\n<channel>\n<title>뽐뿌게시판</title>\n'
for t,no,desc,p in rss_items:
    x += f'<item>\n<title>{t}</title>\n<link>http://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&amp;no={no}</link>\n<description>{desc}</description>\n<author>u</author>\n<pubDate>{p}</pubDate>\n<hits> [0|212|0|0]</hits>\n</item>\n'
x += '</channel></rss>'
open(f"{d}/ppomppu_rss.xml","w",encoding="utf-8").write(x)

row = lambda no, shop, title, cat, ts, cls="baseList bbs_new1 ": f'''<tr align="center" class="{cls}"> <td class="baseList-space baseList-numb" colspan="2">{no}</td> <td align="left" class="baseList-space title"> <a class="baseList-thumb" href="view.php?id=ppomppu&amp;no={no}"><img src="x.jpg"></a><div class="baseList-box"><div class="baseList-cover"><a class="baseList-title " href="view.php?id=ppomppu&amp;page=1&amp;divpage=118&amp;no={no}"><span><em class="baseList-head subject_preface">[{shop}]</em>{title}</span></a></div><small class="baseList-small">[{cat}]</small></div></td> <td class="baseList-space" colspan="2"><div class="list_name">u</div></td> <td class="baseList-space" colspan="2" title="{ts}"><time class="baseList-time">x</time></td> <td class="baseList-space baseList-views" colspan="2">346</td> </tr>'''
notice = '<tr class="baseNotice"><td>공지</td><td><a href="view.php?id=ppomppu&no=1">[공지] 게시판 이용 안내입니다</a></td></tr>'
h = '<html><head><meta charset="euc-kr"></head><body><table>' + notice + \
    row(751369,"롯데온","스타벅스 캡슐커피 대용량 90캡슐+카푸치노 머그 2개 증정 (47,740원/무료)","식품/건강","26.11.24 15:05:58") + \
    row(751340,"컬리","라쿠진 퓨어스팀 올스텐 가열식 가습기 (122,103원/무배)","가전/가구","26.11.24 14:31:02", "baseList bbs_new1  hotpop_bg_color") + \
    row(751333,"롯데온","농심 생생우동 16봉 (24,770원/무료)","식품/건강","26.11.24 14:20:11") + '</table></body></html>'
open(f"{d}/ppomppu_list_1.html","wb").write(h.encode("euc-kr"))

def gn(items):
    s = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><rss version="2.0"><channel><title>Google 뉴스</title>'
    for i,(t,src,p) in enumerate(items):
        s += f'<item><title>{t} - {src}</title><link>https://news.google.com/rss/articles/CBM{i}x?oc=5</link><guid isPermaLink="false">CBM{abs(hash(t))}</guid><pubDate>{p}</pubDate><description>x</description><source url="https://e.com">{src}</source></item>'
    return s + '</channel></rss>'
open(f"{d}/gnews_이마트_행사.xml","w",encoding="utf-8").write(gn([
 ("이마트 주말 신선식품 할인 행사, 참다랑어·감귤·육류 특가 판매","비즈니스포스트","Fri, 20 Nov 2026 00:47:06 GMT"),
 ("이마트 주말 신선식품 할인 행사, 참다랑어·감귤 특가","뉴스1","Fri, 20 Nov 2026 01:10:00 GMT"),
 ("대덕소방서, 이마트 대전복합터미널점서 ‘불조심 강조의 달’ 시민안전 체험행사 개최","FPN-소방방재신문","Tue, 17 Nov 2026 08:00:00 GMT"),
]))
open(f"{d}/gnews_다이슨_할인.xml","w",encoding="utf-8").write(gn([
 ("에어팟 프로 149불·다이슨 청소기 55% 할인…블프 할인 경쟁","미주중앙일보","Mon, 23 Nov 2026 22:04:00 GMT"),
 ("현대백화점 판교점에 '다이슨 뷰티' 특화 스토어 오픈","전자신문","Wed, 18 Nov 2026 00:58:15 GMT"),
]))
