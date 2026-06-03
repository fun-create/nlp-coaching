# -*- coding: utf-8 -*-
"""NLPコーチング ガイドブック PDF ジェネレーター"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                HRFlowable, NextPageTemplate)

# ---- フォント（reportlab内蔵の日本語CIDフォント。外部ファイル不要）----
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))   # ゴシック
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))      # 明朝
G, M = 'HeiseiKakuGo-W5', 'HeiseiMin-W3'

# ---- カラーパレット（アプリと統一）----
BRAND   = colors.HexColor('#2f8f7f')
BRAND_D = colors.HexColor('#226b5f')
BRAND_L = colors.HexColor('#e7f4f1')
ACCENT  = colors.HexColor('#6b6ad6')
ACCENT_L= colors.HexColor('#ececfb')
WARN    = colors.HexColor('#c98a2b')
WARN_L  = colors.HexColor('#fbf2e3')
INK     = colors.HexColor('#23323a')
MUTED   = colors.HexColor('#6b7c85')
LINE    = colors.HexColor('#dbe6e3')
PALE    = colors.HexColor('#f4f7f6')

PW, PH = A4

# ---- スタイル ----
def S(name, **kw):
    base = dict(fontName=G, fontSize=10.5, leading=16, textColor=INK)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_h1     = S('h1', fontSize=20, leading=26, textColor=BRAND_D, spaceAfter=4)
st_h2     = S('h2', fontSize=15, leading=20, textColor=colors.white, spaceBefore=2, spaceAfter=2)
st_h3     = S('h3', fontSize=13, leading=18, textColor=BRAND_D, spaceBefore=10, spaceAfter=4)
st_body   = S('body', fontSize=10.5, leading=17, spaceAfter=6)
st_bodyM  = S('bodyM', fontName=M, fontSize=10.5, leading=17, spaceAfter=6)
st_small  = S('small', fontSize=9, leading=13, textColor=MUTED)
st_lead   = S('lead', fontSize=11, leading=18, textColor=INK, spaceAfter=8)
st_bullet = S('bullet', fontSize=10, leading=15)
st_wname  = S('wname', fontSize=14, leading=18, textColor=colors.white)
st_wen    = S('wen', fontSize=8.5, leading=11, textColor=colors.HexColor('#d8efe9'))
st_meta   = S('meta', fontSize=9, leading=13, textColor=MUTED)
st_script = S('script', fontName=M, fontSize=9.7, leading=15, textColor=colors.HexColor('#33327a'))
st_obs    = S('obs', fontSize=9.3, leading=14, textColor=colors.HexColor('#7a5a18'))
st_steptt = S('steptt', fontSize=10.3, leading=14, textColor=INK)
st_caut   = S('caut', fontSize=9.5, leading=14, textColor=colors.HexColor('#8a4a30'))
st_toc    = S('toc', fontSize=11, leading=20, textColor=INK)
st_cover_t= S('covt', fontName=G, fontSize=30, leading=38, textColor=colors.white, alignment=TA_CENTER)
st_cover_s= S('covs', fontName=M, fontSize=13, leading=20, textColor=colors.HexColor('#d8efe9'), alignment=TA_CENTER)

def diff_label(d): return {1:'入門', 2:'標準', 3:'上級'}[d]

# ============================================================
#  コンテンツデータ
# ============================================================
PRESUPPOSITIONS = [
    ("地図は領土ではない", "人は現実そのものではなく、自分が作った『地図（解釈）』を生きている。地図を描き替えれば体験が変わる。"),
    ("相手の反応がコミュニケーションの意味", "伝えた『つもり』ではなく、相手に伝わった結果がすべて。反応を見て柔軟に変える。"),
    ("失敗はなく、フィードバックがあるだけ", "うまくいかない結果も、次への有益な情報。学びとして活かす。"),
    ("人はその時できる最善の選択をしている", "どんな行動にも肯定的な意図がある。行動と人格を切り分ける。"),
    ("人は変化に必要な資源をすでに持っている", "答えはクライアントの中にある。コーチはそれを引き出す。"),
    ("心と身体はひとつのシステム", "姿勢・呼吸・表情を変えると、感情や思考も変わる。"),
    ("選択肢は多いほどよい", "行き詰まりとは選択肢が1つしかない状態。新しい選択肢を増やす。"),
    ("抵抗は関係（ラポール）不足のサイン", "クライアントが抵抗するのは、ペースが合っていないから。"),
]

CONCEPTS = [
    ("ラポール（信頼関係）",
     "すべての土台。クライアントの呼吸・姿勢・声の調子・言葉づかいにさりげなく合わせる『ペーシング』で安心の場を作り、"
     "信頼が育ったら、こちらが先に変化を示す『リーディング』で望ましい方向へ導く。"),
    ("キャリブレーション（観察）",
     "言葉だけでなく、表情・肌の色・呼吸・声の変化など非言語の微細なサインを観察し、クライアントの内的状態を読み取る。"
     "ワークの効果は、この観察によって確認する。"),
    ("代表システム（VAK）",
     "人は視覚（V）・聴覚（A）・体感覚（K）で世界を体験する。クライアントが多用する感覚に言葉を合わせると伝わりやすい。"
     "『見えてきた』『しっくりくる』などの言葉から優位な感覚を見分ける。"),
    ("サブモダリティ（感覚の質）",
     "イメージの明るさ・大きさ・距離、音の大小、感覚の強さなど、体験を構成する細かな要素。"
     "これを変えると、感情の強さを自在に調整できる。"),
    ("メタモデル（明確化の質問）",
     "『省略・歪曲・一般化』された言葉を、質問で具体的な体験に戻す技法。"
     "『具体的には？』『いつも、例外なく？』『もしできるとしたら？』で思考の制限をほどく。"),
    ("ミルトンモデル（許容的な言葉）",
     "あえて曖昧な言葉を使い、クライアントが自分なりの意味で受け取れる余白を作る。"
     "内的な探索や、リラックス・気づきを促す場面で用いる。"),
    ("アンカリング（条件づけ）",
     "特定の刺激（身体の動きなど）と心理状態を結びつけ、必要なときにその状態を再現する技法。"
     "アンカリング、サークル・オブ・エクセレンスの基礎となる。"),
    ("肯定的意図とパーツ",
     "どんな問題行動の奥にも、本人を守ろうとする肯定的な意図がある。"
     "心の中の『部分（パーツ）』として扱い、対話することで根本的な変化を起こす。"),
]

# 評価6指標
EVAL_METRICS = [
    ("傾聴バランス", "コーチが話しすぎず、クライアントが主役として十分に語れているか。理想はクライアントの発話が5〜7割。"),
    ("質問の質と量", "『どんな』『本当は』など、内的世界を引き出す「開かれた質問」が使えているか。"),
    ("ラポール・受容", "『なるほど』『そうですね』など、受け止め・共感の言葉で安心の場ができているか。"),
    ("クライアントの気づき", "クライアント自身から『そうか』『軽くなった』など、気づき・変化の言葉が生まれているか（最重要）。"),
    ("ワーク適合度", "選んだワーク特有の問いかけ・展開が、会話の中に実際に表れているか。"),
    ("行動・未来志向", "気づきが『次の一歩』『やってみる』など、具体的な行動・未来へつながっているか。"),
]

# ---- 19ワーク（アプリと同一内容）----
WORKS = [
 dict(name="ウェルフォームド・アウトカム", en="Well-Formed Outcome", cat="目標設定", dur=25, diff=1,
   purpose="漠然とした願望を、五感で確認でき実現可能な『整った目標』に変えるNLPの基本ワーク。",
   indication="目標が曖昧、何から手をつけるか分からない、モチベーションが続かないクライアントに最適。",
   steps=[("肯定的な表現にする","『〜したくない』ではなく、どうなりたいかを引き出す。"),
          ("自分で達成できる範囲か確認","他人を変える目標になっていないか確認する。"),
          ("五感での証拠を引き出す","実現時に見える・聞こえる・感じるものを具体化する。"),
          ("状況・文脈を具体化する","いつ・どこで・誰と実現するかを明確にする。"),
          ("今あるリソースを確認","既に持つ力・経験・人脈を承認する。"),
          ("副作用（エコロジー）チェック","手に入れることで失うもの・困る人を確認する。"),
          ("最初の一歩を決める","24時間以内にできる小さな一歩を日時まで決める。")],
   caution="『本当に望んでいるか』を丁寧に確認する。表面的な目標の裏に本当の願いが隠れていることが多い。"),
 dict(name="ニューロ・ロジカルレベル", en="Logical Levels Alignment", cat="自己認識", dur=30, diff=2,
   purpose="環境〜自己認識までの6つの階層を順に辿り、価値観・アイデンティティのレベルで整合を取る。",
   indication="頑張っているのに空回りする、自分軸が定まらない、本質的な変化を起こしたいクライアントに。",
   steps=[("環境","いつ・どこで・誰といる時かを具体化する。"),
          ("行動","その状況で何をしている／したいかを引き出す。"),
          ("能力","用いているスキル・戦略を確認する。"),
          ("信念・価値観","なぜ大切か、何を信じているかを問う。"),
          ("自己認識","それを実現している自分を一言で表す。"),
          ("使命・つながり","自分を超えた貢献・つながりを味わう。"),
          ("統合して降りる","上位の気づきを保ったまま各レベルへ戻り一致させる。")],
   caution="各レベルに十分留まる。急がず、クライアントの内的な変化を待つ。"),
 dict(name="タイムライン", en="Timeline / Future Pacing", cat="時間軸", dur=25, diff=2,
   purpose="過去・現在・未来を空間的な線として扱い、望む未来を先取り体験（フューチャーペース）する。",
   indication="将来に不安がある、目標が現実味を持てない、過去の出来事を整理したいクライアントに。",
   steps=[("タイムラインを描く","過去と未来がどの方向に伸びるかを尊重する。"),
          ("現在地を確認","線上の『今』に立ち、ニュートラルな状態を作る。"),
          ("望む未来へ移動","目標が実現した未来の地点まで進む。"),
          ("未来を五感で味わう","未来の自分として見え・聞こえ・感じるものを語る。"),
          ("未来から現在を振り返る","未来の自分から今の自分へ助言を引き出す。"),
          ("現在へ戻り定着","未来のリソースを現在に統合し行動につなぐ。")],
   caution="つらい過去を扱う時は必ず観察者の立場で。強い感情には無理に踏み込まない。"),
 dict(name="アンカリング", en="Resource Anchoring", cat="状態管理", dur=20, diff=1,
   purpose="自信・安心などの望ましい状態を身体的なトリガーに結びつけ、必要なときに再現する。",
   indication="本番で緊張する、自信を出したい場面がある、感情の波を自分で整えたいクライアントに。",
   steps=[("望む状態を決める","呼び出したい状態を一つに絞る。"),
          ("その状態の記憶を呼び出す","最高に感じた場面をありありと思い出す。"),
          ("五感を強める","見え・聞こえ・体感を鮮やかにする。"),
          ("ピーク時にアンカーを設定","感情の頂点でこぶしを握るなど刺激を入れる。"),
          ("状態を解いて切り替える","一度ニュートラルに戻す（ブレイクステート）。"),
          ("アンカーをテスト","刺激で状態が再現されるか確認する。"),
          ("未来で使う練習","本番場面を想像し、アンカーで臨む。")],
   caution="独特で再現しやすい動作を選ぶ。ピークのタイミングを逃さないことが鍵。"),
 dict(name="リフレーミング", en="Reframing", cat="意味の転換", dur=20, diff=1,
   purpose="出来事の『枠組み』を変え、同じ事実から新しい肯定的な意味を見出す。",
   indication="自分を責めがち、短所が気になる、ネガティブな解釈に縛られているクライアントに。",
   steps=[("気になる事実を明確に","解釈と事実を分けて聞く。"),
          ("その解釈を確認","制限的な意味づけを特定する。"),
          ("内容のリフレーム","同じ事実の別の良い意味を探す。"),
          ("文脈のリフレーム","その特徴が役立つ場面を見つける。"),
          ("肯定的意図を見つける","その反応が何から守ろうとしているか問う。"),
          ("新しい見方を定着","本人の言葉で再定義してもらう。")],
   caution="コーチが押し付けない。本人が『腑に落ちる』リフレームを一緒に見つける。"),
 dict(name="スウィッシュ・パターン", en="Swish Pattern", cat="行動変容", dur=20, diff=2,
   purpose="望ましくない自動反応のイメージを、なりたい自分のイメージへ高速で切り替える。",
   indication="やめたい癖、つい出る反応、自動的なネガティブ反応を変えたいクライアントに。",
   steps=[("トリガー画像を特定","癖が出る直前の光景を思い浮かべる。"),
          ("望む自己像を作る","癖を必要としない理想の姿を魅力的に描く。"),
          ("望む像を小さく隅に置く","2つのイメージを同時に保持する。"),
          ("スウィッシュ！","一瞬で両者を入れ替える。"),
          ("画面をクリア","毎回ブレイクステートを入れる。"),
          ("5〜7回繰り返す","だんだん速く繰り返し自動化する。"),
          ("テスト","元のトリガーで理想像が浮かぶか確認する。")],
   caution="スピードと繰り返しが効果を決める。各回の間に必ずブレイクステートを入れる。"),
 dict(name="ポジション・チェンジ", en="Perceptual Positions", cat="対人関係", dur=25, diff=2,
   purpose="自分・相手・第三者の3つの視点に立ち、対人関係の状況を多角的に捉え直す。",
   indication="特定の相手との関係に悩む、相手の気持ちが分からない、対立を解消したいクライアントに。",
   steps=[("場面を設定","うまくいかない一場面を選ぶ（椅子3つが効果的）。"),
          ("第1ポジション（自分）","自分の視点・感情・ニーズを言語化する。"),
          ("第2ポジション（相手）","相手になりきり、相手から見た自分を語る。"),
          ("第3ポジション（観察者）","公平な第三者として関係のパターンを観る。"),
          ("気づきを統合","3視点の発見を統合する。"),
          ("第1ポジションへ戻る","気づきを持って次の関わり方を決める。")],
   caution="第2ポジションでは相手を批判せず、純粋に相手の世界を体験する。"),
 dict(name="パーツ統合", en="Parts Integration", cat="内的葛藤", dur=30, diff=3,
   purpose="心の中で対立する2つの部分の肯定的意図を見つけ、より高い目的のもとで統合する。",
   indication="『やりたいけどできない』の板挟み、決断できない、相反する気持ちに引き裂かれるクライアントに。",
   steps=[("2つの部分を特定","葛藤の両側をどちらも価値あるものとして扱う。"),
          ("それぞれを手のひらに","各パーツを色・形・重さでイメージ化する。"),
          ("肯定的意図を聞く（右）","本当は何をしてくれているかを深掘りする。"),
          ("肯定的意図を聞く（左）","もう一方の本当の願いを引き出す。"),
          ("共通の上位目的を発見","2つの意図に共通する願いに気づく。"),
          ("両手を合わせて統合","本人のペースで一つに統合する。"),
          ("統合を体に取り込む","一つになった力を胸に取り込み定着させる。")],
   caution="高度なワーク。クライアントのペースを最優先し、無理に統合を急がない。"),
 dict(name="ディズニー・ストラテジー", en="Disney Strategy", cat="発想・計画", dur=30, diff=2,
   purpose="夢想家・現実家・批評家の3つの思考モードを順に使い、夢を現実的な計画へと磨き上げる。",
   indication="アイデアはあるが形にできない、企画を練りたい、計画倒れになりがちなクライアントに。",
   steps=[("3つの場所を用意","物理的に移動して思考モードを切り替える。"),
          ("夢想家","制約を外して理想を自由に広げる。"),
          ("現実家","具体的な手順・必要なものに落とし込む。"),
          ("批評家","人ではなく計画を建設的に批評する。"),
          ("夢想家へ戻り改善","批評を踏まえ案を膨らませる。"),
          ("統合プランを確定","3視点を通した実行プランをまとめる。")],
   caution="各役割になりきり立場を混ぜない。批評家で夢想を潰しすぎないよう循環させる。"),
 dict(name="コア・トランスフォーメーション", en="Core Transformation", cat="深い変容", dur=40, diff=3,
   purpose="問題行動の肯定的意図を何層も辿り、『コアステート（平安・愛・一体感）』に到達して根本から変容する。",
   indication="繰り返す悩み、根深い感情パターン、本質的な自己受容を求めるクライアントに（上級）。",
   steps=[("扱うパターンを選ぶ","変えたい反応・感情を一つ選ぶ。"),
          ("その部分を歓迎する","部分を敵対せず味方として受け入れる。"),
          ("肯定的意図を問う","これを通じて本当は何を得たいか問う。"),
          ("意図の連鎖を辿る","『その先に』を繰り返し深い状態へ進む。"),
          ("コアステートに到達","平安・愛・一体感など根源的な状態を味わう。"),
          ("コアから逆流させる","コアの状態を各層へ流し込み変容させる。"),
          ("日常へ統合","その状態を持って日常を生きる姿を描く。")],
   caution="最も深いワーク。十分な信頼関係と時間が前提。内的プロセスを急かさない。"),
 dict(name="V-Kディソシエーション", en="V-K Dissociation", cat="恐れの解放", dur=30, diff=3,
   purpose="つらい記憶を『映画を見る観察者』の立場から扱い、結びついた強い感情を切り離して和らげる。",
   indication="特定の場面への強い恐れ・苦手意識、嫌な記憶がフラッシュバックするクライアントに（慎重に）。",
   steps=[("安全な状態を作る","安心できる場所をイメージし落ち着く。"),
          ("映画館に座る","記憶をスクリーンに映す観客になる。"),
          ("射影室から眺める","客席の自分を眺める二重の分離を作る。"),
          ("記憶を白黒で再生","小さな白黒映像で最後まで流す。"),
          ("安全な結末まで見る","無事に終わったことを確認する。"),
          ("高速で巻き戻す","カラーで中に入りコミカルに巻き戻す。"),
          ("テストして確認","思い出した時の感じ方の変化を確認する。")],
   caution="トラウマの程度によっては医療・心理の専門家へ。常に安全第一。"),
 dict(name="SCOREモデル", en="SCORE Model", cat="課題整理", dur=25, diff=2,
   purpose="症状・原因・望む成果・資源・効果の5要素で、問題の全体像を構造的に整理する。",
   indication="課題が複雑で絡まっている、何が問題か整理したい、初回の見立てに最適。",
   steps=[("S：症状","表面に出ている困りごとを具体化する。"),
          ("C：原因","奥にある原因を捉える。"),
          ("O：成果","本当はどうなりたいかを明確にする。"),
          ("R：資源","必要な・既にある力を棚卸しする。"),
          ("E：効果","成果の先の良い波及効果を引き出す。"),
          ("全体のつながりを確認","次に取り組む方向性を一緒に決める。")],
   caution="見立てのワーク。方向性を定め、必要に応じて他のワークへつなぐ。"),
 dict(name="サブモダリティ・チェンジ", en="Submodality Change", cat="感情調整", dur=20, diff=2,
   purpose="イメージの『質（明るさ・大きさ・距離・音など）』を調整し、感情の強さをコントロールする。",
   indication="感情に飲まれやすい、特定の記憶が重い、ポジティブな感情を強めたいクライアントに。",
   steps=[("対象の感情を選ぶ","弱めたい／強めたい感情を一つ選ぶ。"),
          ("イメージの質を調べる","映像の大きさ・距離・明るさ・音を確認する。"),
          ("どの要素が効くか発見","変えると感情が大きく動く要素を特定する。"),
          ("望む方向へ調整","楽になる方向へその要素を動かす。"),
          ("固定する","ちょうど良いところでロックする。"),
          ("テスト","元の場面を思い出し変化を確認する。")],
   caution="人により効く要素は異なる。本人固有の『効く要素』を見つけるのが鍵。"),
 dict(name="新行動の創造", en="New Behavior Generator", cat="行動習得", dur=25, diff=2,
   purpose="理想の行動を心の中でリハーサルし、新しい振る舞いを身につけてから現実で実行する。",
   indication="新しい行動を身につけたい、本番前に練習したい、苦手な場面を克服したいクライアントに。",
   steps=[("身につけたい行動を決める","具体的な行動を一つに絞る。"),
          ("お手本を観る","理想的にこなす自分を外から観る。"),
          ("修正する","納得いくまで理想像を編集する。"),
          ("中に入って体験","映像の中に入り内側から体感する。"),
          ("繰り返しリハーサル","自然にできる感覚まで反復する。"),
          ("未来へ結びつける","実際の場面を想像し新行動で臨む。")],
   caution="まず外から観て（理想設計）、次に中に入る（体得）の順序が大切。"),
 dict(name="メタモデル質問", en="Meta Model Questions", cat="明確化", dur=20, diff=1,
   purpose="言葉の『省略・歪み・一般化』を質問で明らかにし、思考の制限を解いて現実を正確に捉え直す。",
   indication="思い込みで身動きが取れない、考えが堂々巡り、漠然とした不安を抱えるクライアントに。",
   steps=[("制限的な発言を捉える","『できない』『いつも』等のパターンに注目する。"),
          ("省略を埋める","『具体的には？』で抜けた情報を尋ねる。"),
          ("一般化を確認","『例外なく？』で過度な一般化を検証する。"),
          ("歪みをほどく","思い込みの根拠を問う。"),
          ("制限の境界を試す","『もしできるとしたら？』で限界を揺らす。"),
          ("新しい選択肢を確認","見え方・選択肢の変化を確認する。")],
   caution="尋問にならないよう、ラポールを保ち、好奇心と敬意をもって問いかける。"),
 dict(name="ストラテジー（戦略の活用）", en="Strategy Elicitation", cat="行動習得", dur=25, diff=2,
   purpose="うまくいっている時の『心の手順（戦略）』を解明し、再現・最適化して望む結果を意図的に作り出す。",
   indication="調子の波が激しい、得意な時とダメな時の差が大きい、成功を再現したいクライアントに。",
   steps=[("うまくいく場面を選ぶ","成功体験を特定する（TOTEの枠で観る）。"),
          ("引き金を特定","何を見て・聞いて・感じて始まるか。"),
          ("心の手順を分解","頭の中の順番をステップで書き出す。"),
          ("完了の合図を確認","『できた』と分かる基準・出口を特定する。"),
          ("うまくいかない時と比較","成功と失敗の分岐点を見つける。"),
          ("最適な戦略を再インストール","成功手順を別場面でも使えるよう般化する。")],
   caution="内的プロセスをコーチの推測で埋めない。本人の手順をそのまま引き出す。"),
 dict(name="サークル・オブ・エクセレンス", en="Circle of Excellence", cat="状態管理", dur=20, diff=1,
   purpose="床に描いた『卓越の輪』に最高の状態を蓄え、必要な場面で踏み込んで一瞬で力を呼び出す空間アンカー。",
   indication="本番・プレッシャー場面で実力を出したい、自信や落ち着きを瞬時に呼び出したいクライアントに。",
   steps=[("輪を描く","足元に色・大きさのある卓越の輪を想定する。"),
          ("最高の状態を思い出す","力を発揮できた時をありありと思い出す。"),
          ("ピークで輪に入る","感覚が高まりきった瞬間に踏み込む。"),
          ("状態を満たす","全身に状態を満たし輪に蓄える。"),
          ("輪から出る","外へ出てニュートラルに戻る。"),
          ("テスト","再び入って状態が戻るか確認する。"),
          ("未来へ持ち出す","輪を畳んで持ち歩く感覚で本番に接続する。")],
   caution="ピークのタイミングが鍵。輪を『携帯できる』感覚にすると実用的。"),
 dict(name="6ステップ・リフレーミング", en="Six-Step Reframing", cat="行動変容", dur=45, diff=3,
   purpose="やめたい行動を生む『元の部分』と対話し、肯定的な意図を保ったまま、『創造的な部分』からより良い代替行動を生み出して定着させる。",
   indication="頭では分かってもやめられない癖・反応、意志の力だけでは変わらない自動的な行動を扱いたいクライアントに。",
   steps=[("変化させる行動・反応を特定","変えたい行動Xを一つ、具体的な場面まで特定する。"),
          ("「元の部分」とのコミュニケーション確立","行動をとらせる部分に感謝し、YES/NOの合図を確立する。"),
          ("プラスの意図を行動から分離","『本当は何をしてくれているの？』と肯定的意図を引き出す（→ブレークステート）。"),
          ("「創造的な部分」が代替案を3つ以上創る","創造的な部分にアクセスし、意図を満たす新案を3つ以上出す（→ブレークステート）。"),
          ("「元の部分」に選択肢を受け入れてもらう","3週間試す責任を合図で確認し、元の部分に感謝する（不同意なら4へ）。"),
          ("エコロジーチェック","抵抗する部分が自他にないか確認（あれば2へ戻る）。"),
          ("未来ペーシング","新案が要る未来の場面を想像し、新パターンを定着・検証する。")],
   caution="上級ワーク。ステップ3・4の後にブレークステートを挟む。合図の確認を丁寧に行い、コーチが答えを決めない。"),
 dict(name="フォビアの迅速治療", en="Fast Phobia Cure", cat="恐れの解放", dur=25, diff=3,
   purpose="恐怖症やパニック反応を、二重に切り離した安全な視点と映像の高速逆再生で短時間で和らげる代表技法。",
   indication="特定の対象・場面への強い恐怖反応（高所・人前・乗り物など）を扱いたいクライアントに（慎重に）。",
   steps=[("安全な状態を確立","安心のアンカーを設定してから始める。"),
          ("映画館に座る","恐怖が起きる前の静止画をスクリーンに映す。"),
          ("射影室へ移る","二重に分離した安全な観察位置を確保する。"),
          ("白黒で最後まで再生","小さな白黒映画で安全な結末まで流す。"),
          ("結末で静止","無事に終わった場面で止める。"),
          ("カラーで高速逆再生","中に入り1〜2秒で巻き戻す（2〜5回）。"),
          ("テストして確認","対象を思い浮かべ感じ方の変化を確認する。")],
   caution="強いトラウマ・臨床的恐怖症は医療／心理の専門家の領域。範囲を超える場合は連携する。"),
]

# ============================================================
#  ページ描画（背景・ヘッダー・フッター）
# ============================================================
def cover_page(c, doc):
    c.saveState()
    # 背景（上半分：BRAND、下半分：BRAND_D）
    c.setFillColor(BRAND_D); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(BRAND);   c.rect(0, PH*0.50, PW, PH*0.50, fill=1, stroke=0)
    # 装飾の円
    c.setFillColor(colors.HexColor('#3aa593')); c.circle(PW*0.88, PH*0.84, 64, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#2a7d6e')); c.circle(PW*0.10, PH*0.20, 88, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#1f5c4e')); c.circle(PW*0.80, PH*0.12, 40, fill=1, stroke=0)

    # ── コンパスマーク（ページ上部中央）──
    cx, cy = PW/2, PH*0.75
    c.setStrokeColor(colors.white); c.setLineWidth(2.6)
    c.circle(cx, cy, 44, fill=0, stroke=1)
    c.setFillColor(colors.white)
    c.saveState(); c.translate(cx, cy)
    p = c.beginPath(); p.moveTo(0,30); p.lineTo(11,0); p.lineTo(0,-30); p.lineTo(-11,0); p.close()
    c.drawPath(p, fill=1, stroke=0); c.restoreState()

    # ── タイトル（コンパスの下）──
    c.setFillColor(colors.white)
    c.setFont(G, 36); c.drawCentredString(PW/2, PH*0.60, 'NLPコーチング')
    c.setFont(G, 36); c.drawCentredString(PW/2, PH*0.52, 'ガイドブック')

    # ── サブタイトル ──
    c.setFont(M, 13); c.setFillColor(colors.HexColor('#d8efe9'))
    c.drawCentredString(PW/2, PH*0.42, 'コーチのための実践ハンドブック')
    c.drawCentredString(PW/2, PH*0.37, '〜 ヒアリングから19のワーク、評価まで 〜')

    # ── 区切り線 ──
    c.setStrokeColor(colors.HexColor('#5bc4b0')); c.setLineWidth(1.2)
    c.line(PW*0.25, PH*0.33, PW*0.75, PH*0.33)

    # ── フッターテキスト ──
    c.setFont(G, 10); c.setFillColor(colors.HexColor('#aadfd6'))
    c.drawCentredString(PW/2, PH*0.12, "NLP Coaching Guide  /  Coach's Companion")

    c.restoreState()

def later_pages(c, doc):
    c.saveState()
    # ヘッダー帯
    c.setFillColor(BRAND); c.rect(0, PH-12*mm, PW, 12*mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont(G, 8.5)
    c.drawString(18*mm, PH-8*mm, "NLPコーチング ガイドブック")
    c.drawRightString(PW-18*mm, PH-8*mm, "コーチ用ガイド")
    # フッター
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(18*mm, 13*mm, PW-18*mm, 13*mm)
    c.setFillColor(MUTED); c.setFont(G, 8)
    c.drawCentredString(PW/2, 9*mm, "— %d —" % doc.page)
    c.restoreState()

# ============================================================
#  フロアブル生成ヘルパー
# ============================================================
def section_title(num, title):
    """章見出し（カラー帯）"""
    t = Table([[Paragraph("<font name='%s' size=11>%s</font>  <font size=15>%s</font>" %
                (G, num, title), st_h2)]], colWidths=[PW-36*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BRAND),
        ('LEFTPADDING',(0,0),(-1,-1),12), ('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('ROUNDEDCORNERS',[5,5,5,5]),
    ]))
    return t

def info_box(text, bg, border, style):
    t = Table([[Paragraph(text, style)]], colWidths=[PW-36*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),0.8,border),
        ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('ROUNDEDCORNERS',[6,6,6,6]),
    ]))
    return t

def work_flowables(i, w):
    els = []
    # ヘッダーカード
    head = Table([[
        Paragraph("%02d" % i, S('wn', fontSize=19, leading=21, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>%s</b><br/><font name='%s' size=8.5 color='#d8efe9'>%s</font>" % (w['name'], G, w['en']), st_wname),
        Paragraph("約%d分<br/>%s" % (w['dur'], diff_label(w['diff'])),
                  S('wd', fontSize=8.5, leading=12, textColor=colors.white, alignment=TA_CENTER)),
    ]], colWidths=[18*mm, (PW-36*mm)-18*mm-22*mm, 22*mm])
    head.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BRAND_D),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LINEAFTER',(0,0),(0,0),0.6,colors.HexColor('#3aa593')),
        ('ROUNDEDCORNERS',[6,6,0,0]),
    ]))
    els.append(head)
    # 目的・適用
    body = Table([
        [Paragraph("<font color='#226b5f'><b>目的</b></font>", st_small),
         Paragraph(w['purpose'], st_body)],
        [Paragraph("<font color='#226b5f'><b>適した場面</b></font>", st_small),
         Paragraph(w['indication'], st_body)],
    ], colWidths=[24*mm, (PW-36*mm)-24*mm])
    body.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),PALE),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,0),0.5,LINE),
    ]))
    els.append(body)
    els.append(Spacer(1,4))
    # ステップ表
    rows = [[Paragraph("<b>進行ステップ</b>", S('sh', fontSize=9.5, textColor=BRAND_D)),
             Paragraph("<b>進行・観察ポイント</b>", S('sh', fontSize=9.5, textColor=BRAND_D))]]
    for n,(tt,obs) in enumerate(w['steps'],1):
        rows.append([
            Paragraph("<font color='#2f8f7f'><b>%d.</b></font> %s" % (n, tt), st_steptt),
            Paragraph(obs, st_obs),
        ])
    stt = Table(rows, colWidths=[(PW-36*mm)*0.42, (PW-36*mm)*0.58])
    sty = [('VALIGN',(0,0),(-1,-1),'TOP'),
           ('BACKGROUND',(0,0),(-1,0),BRAND_L),
           ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
           ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
           ('LINEBELOW',(0,0),(-1,-1),0.4,LINE),
           ('BOX',(0,0),(-1,-1),0.6,LINE),
           ('LINEAFTER',(0,0),(0,-1),0.4,LINE)]
    for r in range(1,len(rows)):
        if r % 2 == 0:
            sty.append(('BACKGROUND',(0,r),(-1,r),colors.HexColor('#fbfdfc')))
    stt.setStyle(TableStyle(sty))
    els.append(stt)
    els.append(Spacer(1,6))
    # 留意点
    els.append(info_box("<b>留意点：</b>"+w['caution'], WARN_L, colors.HexColor('#eed9b0'), st_caut))
    # 1ワーク1ページ開始のためKeepTogetherは不要（ページ分割はreportlabに委ねる）
    return els

# ============================================================
#  ドキュメント組み立て
# ============================================================
def build():
    doc = BaseDocTemplate("guidebook.pdf", pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm,
        title="NLPコーチング ガイドブック", author="NLP Coaching Guide")
    frame = Frame(18*mm, 16*mm, PW-36*mm, PH-34*mm, id='main')
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=[frame], onPage=cover_page),
        PageTemplate(id='body',  frames=[frame], onPage=later_pages),
    ])

    story = []
    # 表紙はすべてcanvasで描画済み → storyには何も入れず次ページでbodyへ切替
    story.append(NextPageTemplate('body'))
    story.append(PageBreak())

    # ----- 目次 -----
    story.append(Paragraph("目次", st_h1))
    story.append(HRFlowable(width="100%", thickness=1.2, color=BRAND, spaceAfter=10))
    toc = [
        "1.  はじめに 〜 本書の使い方",
        "2.  NLPコーチングとは",
        "3.  NLPの前提（プリサポジション）",
        "4.  コーチングの基本姿勢とコア概念",
        "5.  セッションの4ステップ",
        "6.  ワーク・カタログ（全19種）",
        "7.  会話データの評価 6つの視点",
        "8.  倫理と留意点",
    ]
    for t in toc:
        story.append(Paragraph(t, st_toc))
    story.append(PageBreak())

    # ----- 1. はじめに -----
    story.append(section_title("01", "はじめに 〜 本書の使い方"))
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "本書は、NLP（神経言語プログラミング）コーチングを実践するコーチのためのハンドブックです。"
        "クライアントの課題をヒアリングし、最適なワークを選び、リアルタイムで進行し、"
        "セッション後に振り返るまでの一連の流れを、付属アプリ『NLPコーチング ガイド』と連動して支えます。", st_lead))
    story.append(info_box(
        "<b>本書とアプリの関係：</b>アプリは現場での進行（台本・チェックリスト・タイマー）と評価・記録を担い、"
        "本書は各ワークの背景・要点・留意点をまとめた「知識の土台」です。"
        "セッション前の準備や学びの振り返りに本書を、セッション中の進行にアプリをご活用ください。",
        BRAND_L, colors.HexColor('#cfe7e1'), st_body))
    story.append(Spacer(1,6))
    story.append(info_box(
        "<b>大切な前提：</b>NLPコーチングは医療・心理療法の代替ではありません。"
        "クライアントの安全と尊厳を最優先し、コーチの範囲を超える場合は専門家と連携してください。",
        WARN_L, colors.HexColor('#eed9b0'), st_caut))
    story.append(PageBreak())

    # ----- 2. NLPコーチングとは -----
    story.append(section_title("02", "NLPコーチングとは"))
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "NLP（Neuro-Linguistic Programming／神経言語プログラミング）は、1970年代に言語学者ジョン・グリンダーと"
        "リチャード・バンドラーが、優れたセラピストたちの「卓越のパターン」を研究してまとめた実践的な体系です。"
        "『神経（五感の体験）』『言語（言葉）』『プログラミング（くり返される反応パターン）』の関係を扱います。", st_bodyM))
    story.append(Paragraph(
        "NLPコーチングは、この体系をコーチングに応用し、クライアントが<b>望む状態（アウトカム）</b>を明確にし、"
        "すでに持っている内的な<b>資源（リソース）</b>を引き出して、思考・感情・行動のパターンを"
        "望ましい方向へ書き替えていくアプローチです。"
        "コーチは「答えを与える人」ではなく、クライアント自身の変化を引き出す「案内人」です。", st_bodyM))
    story.append(Spacer(1,4))
    story.append(info_box(
        "<b>現状（Present State）</b> から <b>望む状態（Desired State）</b> へ。<br/>"
        "その移行を可能にするのが<b>リソース</b>であり、ワークはリソースへアクセスする具体的な道具です。",
        PALE, LINE, st_body))
    story.append(PageBreak())

    # ----- 3. 前提 -----
    story.append(section_title("03", "NLPの前提（プリサポジション）"))
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "NLPには、コーチが持つと関わりが豊かになる「前提」があります。事実というより、"
        "「そう考えると役に立つ」という心構えです。", st_body))
    story.append(Spacer(1,4))
    rows = [[Paragraph("<b>前提</b>", S('p',fontSize=9.5,textColor=colors.white)),
             Paragraph("<b>意味</b>", S('p',fontSize=9.5,textColor=colors.white))]]
    for t,d in PRESUPPOSITIONS:
        rows.append([Paragraph("<b>%s</b>"%t, st_steptt), Paragraph(d, st_body)])
    tb = Table(rows, colWidths=[(PW-36*mm)*0.36,(PW-36*mm)*0.64])
    sty=[('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),BRAND),
         ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
         ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
         ('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE)]
    for r in range(1,len(rows)):
        if r%2==0: sty.append(('BACKGROUND',(0,r),(-1,r),PALE))
    tb.setStyle(TableStyle(sty))
    story.append(tb)
    story.append(PageBreak())

    # ----- 4. 基本姿勢とコア概念 -----
    story.append(section_title("04", "コーチングの基本姿勢とコア概念"))
    story.append(Spacer(1,8))
    for t,d in CONCEPTS:
        story.append(Paragraph(t, st_h3))
        story.append(Paragraph(d, st_body))
    story.append(PageBreak())

    # ----- 5. 4ステップ -----
    story.append(section_title("05", "セッションの4ステップ"))
    story.append(Spacer(1,8))
    steps4 = [
        ("① ヒアリング","現状と望む状態を引き出し、課題の核を捉える。メタモデルの質問で曖昧さを具体化し、課題の領域を見立てる。"),
        ("② ワーク提案","課題領域と強度から、相性の良いワークを複数提案。クライアントの反応を見ながら一緒に選ぶ。"),
        ("③ 進行ガイド","台本（声かけ例）と観察ポイントを手がかりに、リアルタイムでワークを進める。キャリブレーションで効果を確認。"),
        ("④ 評価・記録","ワーク後の会話を振り返り、傾聴・気づき・行動化などの観点で評価。履歴として残し、次回へつなぐ。"),
    ]
    for t,d in steps4:
        card = Table([[Paragraph("<b>%s</b>"%t, S('s4',fontSize=12,textColor=BRAND_D)),
                       Paragraph(d, st_body)]], colWidths=[34*mm,(PW-36*mm)-34*mm])
        card.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('BACKGROUND',(0,0),(0,0),BRAND_L),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('BOX',(0,0),(-1,-1),0.6,LINE)]))
        story.append(card); story.append(Spacer(1,6))
    story.append(PageBreak())

    # ----- 6. ワークカタログ（導入ページ）-----
    story.append(section_title("06", "ワーク・カタログ（全19種）"))
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "現場で使う代表的な19のワークを、目的・適した場面・進行ステップ・留意点とともにまとめます。"
        u"各ステップの「声かけ例」はアプリの進行ガイドに収録しています。", st_body))
    story.append(PageBreak())

    # ----- ワーク（1ワーク1ページ開始）-----
    for i,w in enumerate(WORKS,1):
        fl = work_flowables(i,w)
        if isinstance(fl,list): story.extend(fl)
        else: story.append(fl)
        story.append(PageBreak())

    # ----- 7. 評価の視点 -----
    story.append(section_title("07", "会話データの評価 6つの視点"))
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "アプリはワーク後の会話データを読み込み、以下の6つの視点でセッションの質を可視化します。"
        "スコアは「良し悪しの判定」ではなく、次回への気づきを得るための鏡としてご活用ください。", st_body))
    story.append(Spacer(1,4))
    rows=[[Paragraph("<b>視点</b>",S('e',fontSize=9.5,textColor=colors.white)),
           Paragraph("<b>見ているもの</b>",S('e',fontSize=9.5,textColor=colors.white))]]
    for t,d in EVAL_METRICS:
        rows.append([Paragraph("<b>%s</b>"%t,st_steptt),Paragraph(d,st_body)])
    tb=Table(rows,colWidths=[(PW-36*mm)*0.30,(PW-36*mm)*0.70])
    sty=[('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),ACCENT),
         ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
         ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
         ('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE)]
    for r in range(1,len(rows)):
        if r%2==0: sty.append(('BACKGROUND',(0,r),(-1,r),ACCENT_L))
    tb.setStyle(TableStyle(sty))
    story.append(tb)
    story.append(Spacer(1,8))
    story.append(info_box(
        "<b>フィードバック資料：</b>評価後、アプリから<b>クライアント向け</b>（課題整理とワーク内容のまとめ）と"
        "<b>コーチ向け</b>（評価詳細と次回への重点）の2種類のPDFを出力できます。",
        BRAND_L, colors.HexColor('#cfe7e1'), st_body))
    story.append(PageBreak())

    # ----- 8. 倫理 -----
    story.append(section_title("08", "倫理と留意点"))
    story.append(Spacer(1,8))
    ethics = [
        ("安全と尊厳の最優先","クライアントの心身の安全を最優先する。不安・抵抗のサインを見逃さない。"),
        ("専門領域の境界","強いトラウマ・うつ・依存など臨床的な課題は医療／心理の専門家の領域。範囲を超える場合は紹介・連携する。"),
        ("同意とペース","ワークは必ず同意のもとで。深いワークほどクライアントのペースを尊重し、急かさない。"),
        ("守秘義務","会話データ・記録は厳重に管理する。本アプリのデータは端末内に保存され、外部送信されない。"),
        ("押し付けない","コーチの解釈や正解を押し付けない。答えはクライアントの中にあるという前提に立つ。"),
        ("自己研鑽","コーチ自身が学び続け、定期的に自分のセッションを振り返る。"),
    ]
    for t,d in ethics:
        story.append(Paragraph("● <b>%s</b>"%t, S('et',fontSize=11,textColor=BRAND_D,spaceBefore=6)))
        story.append(Paragraph(d, st_body))
    story.append(Spacer(1,16))
    story.append(HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=10))
    story.append(Paragraph(
        "クライアントの中には、すでに変化に必要なすべての資源があります。"
        "コーチの役割は、その力を信じ、引き出すこと。本書とアプリが、その実践の一助となれば幸いです。",
        S('end',fontName=M,fontSize=11,leading=18,textColor=INK,alignment=TA_CENTER)))
    story.append(Spacer(1,8))
    story.append(Paragraph("NLP Coaching Guide", S('sig',fontSize=10,textColor=MUTED,alignment=TA_CENTER)))

    doc.build(story)
    print("guidebook.pdf を生成しました")

if __name__ == "__main__":
    build()
