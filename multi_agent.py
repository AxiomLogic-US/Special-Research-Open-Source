import os
import requests
from openai import OpenAI

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHANNEL = os.environ.get("TG_CHANNEL")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY", "AxiomLogic-US/Special-Research-Open-Source")

def send_telegram(text):
    if not TG_TOKEN or not TG_CHANNEL:
        print("Telegram токен или канал не настроены.")
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHANNEL,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print(f"Статус отправки части в Telegram: {response.status_code}")

# --- АГЕНТ 1: Очистка и порядок в репозитории ---
def agent_cleaner():
    print("🧹 [Агент-Чистильщик] Проверка репозитория и наведение порядка...")
    if not GITHUB_TOKEN or not REPO_NAME:
        return "GitHub токен недоступен для очистки."

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    deleted_count = 0
    
    # 1. Проверяем папку .github/workflows
    workflows_url = f"https://api.github.com/repos/{REPO_NAME}/contents/.github/workflows"
    resp_wf = requests.get(workflows_url, headers=headers)
    if resp_wf.status_code == 200:
        for file in resp_wf.json():
            file_name = file["name"]
            if file_name.endswith(".yml") and file_name not in ["main.yml"]:
                delete_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file['path']}"
                delete_data = {
                    "message": f"Multi-Agent Cleanup: remove {file_name}",
                    "sha": file["sha"],
                    "branch": "main"
                }
                del_res = requests.delete(delete_url, headers=headers, json=delete_data)
                if del_res.status_code in [200, 204]:
                    deleted_count += 1

    # 2. Проверяем корень репозитория на наличие случайных .yml файлов
    root_url = f"https://api.github.com/repos/{REPO_NAME}/contents"
    resp_root = requests.get(root_url, headers=headers)
    if resp_root.status_code == 200:
        for file in resp_root.json():
            file_name = file["name"]
            if file_name.endswith(".yml") and file["type"] == "file":
                delete_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file['path']}"
                delete_data = {
                    "message": f"Multi-Agent Cleanup: remove root {file_name}",
                    "sha": file["sha"],
                    "branch": "main"
                }
                del_res = requests.delete(delete_url, headers=headers, json=delete_data)
                if del_res.status_code in [200, 204]:
                    deleted_count += 1

    cleaned_info = f"Удалено мусорных файлов воркфлоу: {deleted_count}."
    print(cleaned_info)
    return cleaned_info

# --- АГЕНТ 2: Исследователь публикаций ---
def agent_researcher():
    print("🔬 [Агент-Исследователь] Сканирование публикаций...")
    if not GITHUB_TOKEN or not REPO_NAME:
        return "Базовые разработки: декарбонизация CO2, мутации белков, резонанс."

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    owner = REPO_NAME.split("/")[0]
    
    repos_url = f"https://api.github.com/users/{owner}/repos?per_type=public&sort=updated"
    response = requests.get(repos_url, headers=headers)
    
    context = ""
    if response.status_code == 200:
        repos = response.json()
        for repo in repos[:3]:
            repo_name = repo["name"]
            context += f"\n- Репозиторий: {repo_name}\n"
            contents_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents"
            c_res = requests.get(contents_url, headers=headers)
            if c_res.status_code == 200:
                for item in c_res.json()[:5]:
                    if item["type"] == "file" and item["name"].endswith((".md", ".txt")):
                        f_res = requests.get(item["download_url"])
                        if f_res.status_code == 200:
                            context += f"  {item['name']}:\n{f_res.text[:400]}\n"
                            
    if len(context) > 2500:
        context = context[:2500]
        
    return context if context else "Базовые открытия: декарбонизация CO2, мутации белков."

# --- АГЕНТ 3: Бизнес-Менеджер и пошаговая отправка ---
def run_ai_agents():
    print("🚀 Запуск мультиагентного комплекса с разделением по темам...")

    if not GROQ_API_KEY:
        print("Ошибка: GROQ_API_KEY не найден!")
        return

    cleanup_status = agent_cleaner()
    research_data = agent_researcher()

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )

    # --- ТЕМА 1: Отчет по аудиту и порядку ---
    msg_part1 = (
        f"🧹 *[Тема 1/3] Аудит репозитория*\n\n"
        f"• Статус очистки: {cleanup_status}\n"
        f"• Инфраструктура GitHub Actions приведена в актуальное состояние."
    )
    send_telegram(msg_part1)

    # --- ТЕМА 2: Анализ научных открытий через ИИ ---
    prompt_science = (
        f"Ты — ведущий ИИ-архитектор. Вот данные из репозиториев:\n{research_data}\n\n"
        "Кратко и структурировано проанализируй ключевые открытия (мутации, декарбонизация) без воды."
    )
    resp_science = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt_science}],
        max_tokens=400
    )
    science_analysis = resp_science.choices[0].message.content

    msg_part2 = (
        f"🔬 *[Тема 2/3] Анализ научных открытий*\n\n"
        f"{science_analysis}"
    )
    send_telegram(msg_part2)

    # --- ТЕМА 3: Коммерческий оффер и бизнес-стратегия ---
    prompt_business = (
        f"Вот данные разработок:\n{research_data}\n\n"
        "Сформируй жесткий коммерческий оффер для крупного бизнеса (штрафы за CO2, фармкомпании): "
        "как клиенты могут безопасно заказать расчет через наш закрытый черный ящик. Кратко, без воды."
    )
    resp_business = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt_business}],
        max_tokens=400
    )
    business_offer = resp_business.choices[0].message.content

    msg_part3 = (
        f"💼 *[Тема 3/3] Коммерческий оффер и рынок*\n\n"
        f"{business_offer}\n\n"
        f"_Система полностью готова к приему клиентских задач._"
    )
    send_telegram(msg_part3)

    print("✅ Все тематические части отчета успешно отправлены в Telegram!")

if __name__ == "__main__":
    run_ai_agents()
