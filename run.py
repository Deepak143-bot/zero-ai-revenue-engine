import json, os, re, sys, urllib.parse, urllib.request, datetime, xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TODAY=datetime.date.today().isoformat()
topics=json.loads((ROOT/"data/topics.json").read_text(encoding="utf-8"))["topics"]

def get(url, timeout=20):
    req=urllib.request.Request(url, headers={"User-Agent":"ZeroAIRevenueEngine/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def google_news(topic):
    q=urllib.parse.quote(topic)
    url=f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        root=ET.fromstring(get(url))
        out=[]
        for item in root.findall(".//item")[:8]:
            title=item.findtext("title","").strip()
            link=item.findtext("link","").strip()
            pub=item.findtext("pubDate","").strip()
            if title:
                out.append({"title":title,"link":link,"published":pub})
        return out
    except Exception as e:
        return [{"title":f"RSS error for {topic}: {e}","link":"","published":""}]

signals=[]
for topic in topics:
    for x in google_news(topic):
        x["topic"]=topic
        signals.append(x)

prompt=f"""
You are the strategy engine for a zero-budget, legitimate AI micro-business operated by one person using an Android phone.
Current date: {TODAY}

Analyze these public news/search signals. Do NOT assume that news popularity equals buying demand.
Find up to 5 opportunities that have a plausible paying customer and can be started with ₹0 upfront.

For each opportunity return:
- opportunity
- target_buyer
- problem
- evidence_from_signals
- product_or_service
- suggested_test_price_in_INR
- fastest_24_hour_test
- creation_workflow_using_free_or_existing_AI
- listing_title
- listing_description
- 3_short_marketing_posts
- what_must_be_verified
- copyright_or_policy_risk
- automation_score_1_to_10
- revenue_potential_score_1_to_10
- confidence_low_medium_high

Important:
- Never promise income.
- Do not recommend spam, fake engagement, copyright infringement, credential theft, deceptive reviews, or bypassing platform restrictions.
- Prefer digital products or useful services that can be created legally.
- Distinguish evidence from inference.
- Return JSON only as:
{{"opportunities":[...]}}
Signals:
{json.dumps(signals[:80], ensure_ascii=False)}
"""

def call_gemini(prompt):
    key=os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    # Gemini API endpoint. Model can be changed in one place if Google's free model lineup changes.
    model=os.environ.get("GEMINI_MODEL","gemini-2.5-flash")
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(key)}"
    body={"contents":[{"parts":[{"text":prompt}]}],
          "generationConfig":{"responseMimeType":"application/json","temperature":0.3}}
    req=urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data=json.loads(r.read().decode())
    text=data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

try:
    result=call_gemini(prompt)
except Exception as e:
    result={"opportunities":[],"error":f"Gemini call failed: {e}"}

if result is None:
    # Safe no-key fallback: identify repeated topics without pretending it is AI research.
    counts={}
    for s in signals:
        counts[s["topic"]]=counts.get(s["topic"],0)+1
    ranked=sorted(counts.items(), key=lambda x:x[1], reverse=True)[:5]
    result={"opportunities":[{
        "opportunity":f"Validate demand around: {topic}",
        "target_buyer":"To be researched manually",
        "problem":"Repeated public signals suggest this topic is worth testing; this is not proof of demand.",
        "evidence_from_signals":f"{count} RSS items collected",
        "product_or_service":"Create a small useful template/service and test with real buyers.",
        "suggested_test_price_in_INR":299,
        "fastest_24_hour_test":"Create one sample, show it to 10 relevant prospects, record responses.",
        "creation_workflow_using_free_or_existing_AI":"Use ChatGPT/manual tools to draft and refine the sample.",
        "listing_title":f"Starter {topic} toolkit",
        "listing_description":"A small, practical starter resource. Verify demand and originality before selling.",
        "3_short_marketing_posts":["Problem → solution → sample → CTA","Show one useful page/feature","Ask target users what they would pay for"],
        "what_must_be_verified":"Buyer demand, platform rules, originality, licensing, pricing.",
        "copyright_or_policy_risk":"Do not copy protected material or imply affiliation.",
        "automation_score_1_to_10":4,
        "revenue_potential_score_1_to_10":4,
        "confidence_low_medium_high":"low"
    } for topic,count in ranked]}

reports_dir=ROOT/"reports"
reports_dir.mkdir(parents=True, exist_ok=True)
out=reports_dir/f"{TODAY}.json"
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

md=["# Zero-Cost AI Revenue Engine — "+TODAY,"","Generated from public RSS signals. This is an opportunity queue, not a guarantee of demand or income.",""]
for i,o in enumerate(result.get("opportunities",[]),1):
    md += [f"## {i}. {o.get('opportunity','')}",
           f"**Buyer:** {o.get('target_buyer','')}",
           f"**Problem:** {o.get('problem','')}",
           f"**Evidence:** {o.get('evidence_from_signals','')}",
           f"**Offer:** {o.get('product_or_service','')}",
           f"**Test price:** ₹{o.get('suggested_test_price_in_INR','')}",
           f"**24h test:** {o.get('fastest_24_hour_test','')}",
           f"**Automation:** {o.get('automation_score_1_to_10','')}/10 | **Revenue potential:** {o.get('revenue_potential_score_1_to_10','')}/10",
           f"**Confidence:** {o.get('confidence_low_medium_high','')}",
           "",f"### Listing",o.get("listing_title",""),o.get("listing_description",""),
           "","### Marketing",*(f"- {x}" for x in o.get("3_short_marketing_posts",[])),
           "","### Verify before publishing",o.get("what_must_be_verified",""),
           "","### Risk",o.get("copyright_or_policy_risk",""),""]
(reports_dir/f"{TODAY}.md").write_text("\n".join(md),encoding="utf-8")
print(f"Created {out}")
