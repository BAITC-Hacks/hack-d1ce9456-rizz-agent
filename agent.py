def classify(message: str) -> tuple[Category, str]:
    """Определяет категорию: справка, жалоба или другое."""
    text = message.lower()

    complaint_words = (
        "очеред", "холодн", "пропал", "не работает", "плохо",
        "жалоб", "проблем", "не могу", "ошибк",
    )
    info_words = (
        "как получить", "где", "справк", "парковк", "записаться",
        "консультаци", "расписани", "когда", "можно ли",
    )

    if contains_any(text, complaint_words):
        return "жалоба", "обнаружены слова, указывающие на проблему или недовольство"
    if contains_any(text, info_words) or "?" in text:
        return "справка", "обнаружен информационный запрос"
    return "другое", "не найдено признаков справки или жалобы"


def draft_response(message: str, category: Category) -> str:
    """Готовит безопасный и полезный черновик ответа на русском языке."""
    text = message.lower()

    if category == "жалоба":
        if "wi-fi" in text or "wifi" in text:
            return (
                "Спасибо, что сообщили. Передадим информацию о Wi-Fi в корпусе B "
                "технической службе. Пожалуйста, уточните этаж и время, когда заметили проблему."
            )
        if "столов" in text or "еда" in text or "очеред" in text:
            return (
                "Спасибо за обратную связь. Передадим замечание администрации столовой. "
                "Уточните, пожалуйста, время посещения и что именно было холодным — это поможет разобраться."
            )
        return "Спасибо за сообщение. Мы зарегистрировали проблему и передадим её ответственным специалистам."

    if category == "справка":
        if "справк" in text and "учёб" in text:
            return (
                "Справку о месте учёбы обычно можно заказать в деканате или через личный кабинет студента. "
                "Возьмите с собой документ, удостоверяющий личность, и уточните срок готовности в деканате."
            )
        if "консультаци" in text:
            return (
                "Чтобы записаться на консультацию на завтра, напишите преподавателю или обратитесь на кафедру. "
                "Укажите предмет, удобное время и группу."
            )
        if "парковк" in text:
            return (
                "Для гостей предусмотрена гостевая парковка. Рекомендуем уточнить схему въезда и наличие мест "
                "у службы охраны перед визитом."
            )
        return "Спасибо за вопрос. Уточните, пожалуйста, детали обращения, и мы подскажем порядок действий."

    return "Спасибо за обращение. Уточните, пожалуйста, ваш вопрос, чтобы мы могли направить его нужному специалисту."


def process(message: str) -> Decision:
    category, reason = classify(message)
    return Decision(category, reason, draft_response(message, category))


def read_messages(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Файл с обращениями не найден: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="ИИ-агент для классификации обращений")
    parser.add_argument("--input", type=Path, default=Path("messages.txt"), help="путь к файлу обращений")
    args = parser.parse_args()

    for number, message in enumerate(read_messages(args.input), start=1):
        decision = process(message)
        print(f"Обращение {number}: {message}")
        print(f"Категория: {decision.category}")
        print(f"Обоснование: {decision.reason}")
        print(f"Черновик ответа: {decision.response}")
        print("-" * 72)


if __name__ == "__main__":
    main()
