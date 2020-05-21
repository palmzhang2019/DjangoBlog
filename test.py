import re

from bs4 import BeautifulSoup
from django.utils.html import escape, strip_tags

s = """
<div class="hdr-container" style='margin:0px;padding:0px;color:#222F3A;font-family:NSimSun, SimSun, PMingLiU, Arial, Helvetica, "font-size:16px;background-color:#FFFFFF;'>
<div class="row" style="margin:0px -12px;padding:0px;">
<p>
<p>
<span class="caption" style="color:#768492;font-size:14px;"><img alt="" src="/media/addArticleImage/0FF199C8-3B6C-4B35-8583-2399A69F3833_w1023_r1_s.jpg"/><br/>
</span>
</p>
<p>
<span class="caption" style="color:#768492;font-size:14px;">图为纽约曼哈顿华尔街的标志。（2020年3月9日）</span>
</p>
</p>
</div>
</div>
<div class="body-container" style='margin:0px;padding:0px;color:#222F3A;font-family:NSimSun, SimSun, PMingLiU, Arial, Helvetica, "font-size:16px;background-color:#FFFFFF;'>
<div class="row" style="margin:0px -12px;padding:0px;">
<div class="col-xs-12 col-sm-12 col-md-10 col-lg-10 pull-right" style="margin:0px;padding:0px 12px;">
<div class="row" style="margin:0px -12px;padding:0px;">
<div class="col-xs-12 col-sm-12 col-md-8 col-lg-8 pull-left bottom-offset content-offset" style="margin:0px;padding:0px 36px 3em 12px;">
<div class="content-floated-wrap fb-quotable" id="article-content" style="margin:0px;padding:0px;">
<div class="wsw" style="margin:0px;padding:0px 0px 16px;">
<p>
								受新冠疫苗取得进展以及美联储或采取进一步刺激措施的提振，美国股市星期一（5月18日）乘势暴涨。
							</p>
<p>
								截至收盘，道琼斯工业平均指数和标准普尔500指数均录得逾一个多月以来最大单日涨幅。道指上涨911.95点，涨幅3.85%，标普500指数涨90.21点，收于涨幅3.15%。纳斯达克综合指数涨220.27点，涨幅2.44%。
							</p>
<p>
								美国生物技术公司Moderna星期一公布了早期新冠疫苗人体试验数据，结果令人鼓舞。数据显示mRNA-1273疫苗受试者产生了抗体，总体来说，mRNA-1273是安全且耐受性良好的。
							</p>
<p>
								共45名受试者分为三组，每组15人，分别接受了25微克、100微克和250微克剂量的mRNA-1273疫苗接种。参与者需接种两剂疫苗，当中间隔大约一个月。
							</p>
<p>
								受试者在接受第二次注射的大约14天后，25微克剂量受试者体内产生的抗体水平与同一试验中检测的新冠康复者血清样本中的水平相同。100微克的参与者体内产生的抗体甚至“明显超过”了新冠康复者血清样本中的水平。250微克剂量组的数据尚不清楚。
							</p>
<p>
								目前的数据显示，有8人体内产生了中和抗体（neutralizing antibodies）。疫苗产生的病毒中和抗体类似于在新冠康复患者体内发现的抗体，这种抗体据信有利于预防新冠感染。其他参与者的中和抗体数据尚不清楚。
							</p>
<p>
								mRNA-1273由Moderna公司与美国国家过敏与传染病研究所（NIAID）疫苗研究中心（VRC）的研究人员联合开发。
							</p>
<p>
								公司还表示，将很快开始第二阶段的测试，届时将有600人参与。第三阶段的临床试验预计将在7月开始。
							</p>
<p>
								公司首席医务官塔尔·扎克斯(Tal Zaks)告诉美国有线电视新闻网（CNN），如果未来的研究进展顺利，公司的疫苗最早将于明年1月上市。
							</p>
<p>
								美联储或启动新的刺激措施也刺激了股市大涨。美联储主席鲍威尔（Jerome Powell）星期日在美国哥伦比亚广播公司（CSB）节目《60分钟》上说，美联储仍有可能在今年下半年采取更多措施，以减轻新冠肺炎疫情对经济造成的冲击。
							</p>
<p>
								鲍威尔说，“我们可以做的还有很多” ，我们的“弹药”远没有用尽。
							</p>
<p>
								他还表示：“我们可以做更多的事情来支持经济，我们承诺尽一切努力，只要我们需要。”
							</p>
<p>
								他也说，美国失业率可能攀升20%到25%，经济要能够恢复，可能得花一段时间，假设没有第二波疫情，经济可望在今年下半年稳步回升。
							</p>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
"""


ret = re.search(r'src="/media/(\w+/.*?.\w{3,4})"', s)
print( ret.groups()[0])