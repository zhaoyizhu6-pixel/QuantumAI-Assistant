from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import random, json, os
import uvicorn

# ==========================
# QuantumAI 助教 · v2.4-final
# 功能：
#   ✅ 自动加载 chat.html / bloch.html
#   ✅ 双路由兼容 (/chat, /api/chat)
#   ✅ 用户记忆持久化 memory.json
#   ✅ 智能追问澄清 + 坦诚拒答
# ==========================

app = FastAPI(title="QuantumAI 助教 · v2.4-final", version="2.4")

# ---- 前端访问配置 ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态资源路径
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# ==========================
# 记忆加载与保存
# ==========================
MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

user_memory = load_memory()

# 内置知识库
base_knowledge = {
    "bloch": "Bloch 球是单量子比特纯态的几何表示，每个点对应一个量子态方向。",
    "量子": "量子是能量的最小单位，是微观世界的基本粒子。",
    "叠加": "量子叠加表示量子系统处于多个状态的线性组合中。",
    "记忆": "量子记忆是一种利用量子叠加和纠缠来存储信息的装置。"
}

# ==========================
# 页面路由
# ==========================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/bloch", response_class=HTMLResponse)
async def bloch_page(request: Request):
    # 渲染 bloch.html 页面
    if os.path.exists("bloch.html"):
        with open("bloch.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    else:
        return JSONResponse({"detail": "Bloch 页面未找到"}, status_code=404)

# ==========================
# 知识检索
# ==========================
def search_knowledge(query: str):
    q = query.lower()
    for k, v in user_memory.items():
        if k in q:
            return f"(来自你教我的记忆) {v}", 0.95
    for k, v in base_knowledge.items():
        if k in q:
            return v, 0.9
    return "", 0.1

# ==========================
# 主对话逻辑
# ==========================
@app.post("/api/chat")
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").strip()
    session = data.get("session", {})
    state = session.get("state", "normal")
    clarification_round = session.get("clarification_round", 0)
    pending_teach = session.get("pending_teach", None)

    if state == "teaching" and pending_teach:
        concept = pending_teach
        user_memory[concept] = user_input
        save_memory(user_memory)
        return JSONResponse({
            "reply": f"我记住了～'{concept}' 是你定义的：{user_input}",
            "session": {"state": "normal"}
        })

    if state == "normal":
        answer, confidence = search_knowledge(user_input)
        if confidence > 0.35:
            return JSONResponse({"reply": answer, "session": {"state": "normal"}})
        else:
            prompt = random.choice([
                "我不太确定你的意思，可以再具体一点吗？",
                "这个问题有点模糊，你能再说说具体想问哪部分吗？",
                "我没太明白，你指的是哪种情况？能再解释一下吗？"
            ])
            return JSONResponse({
                "reply": prompt,
                "session": {"state": "clarifying", "clarification_round": 1, "last_query": user_input}
            })

    elif state == "clarifying":
        last_query = session.get("last_query", "")
        clarification_round = session.get("clarification_round", 1)
        merged_query = last_query + " " + user_input
        answer, confidence = search_knowledge(merged_query)

        if confidence > 0.35:
            return JSONResponse({"reply": answer, "session": {"state": "normal"}})
        elif clarification_round >= 2:
            teach_prompt = (
                f"我理解了你在说“{last_query}”，但我还不知道这是什么意思。"
                "你愿意教我这个概念的含义吗？(是/否)"
            )
            return JSONResponse({
                "reply": teach_prompt,
                "session": {"state": "ask_teach", "pending_teach": last_query}
            })
        else:
            prompt = random.choice([
                "我还是有点不太确定，你能换个角度再说说吗？",
                "我可能还没完全理解，你能再补充一点细节吗？"
            ])
            return JSONResponse({
                "reply": prompt,
                "session": {
                    "state": "clarifying",
                    "clarification_round": clarification_round + 1,
                    "last_query": merged_query
                }
            })

    elif state == "ask_teach":
        pending_teach = session.get("pending_teach")
        if user_input.lower() in ["是", "好的", "行", "当然", "可以", "好呀"]:
            return JSONResponse({
                "reply": f"那你来说说，'{pending_teach}' 是什么意思？",
                "session": {"state": "teaching", "pending_teach": pending_teach}
            })
        else:
            return JSONResponse({
                "reply": "明白啦，那我暂时就记住我不知道这个问题😅",
                "session": {"state": "normal"}
            })

    else:
        return JSONResponse({
            "reply": "出现未知状态，请重新提问。",
            "session": {"state": "normal"}
        })

# ==========================
# 启动服务器
# ==========================
if __name__ == "__main__":
    print("✅ QuantumAI 助教 v2.4-final 启动中...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
