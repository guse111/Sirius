from transformers import MBartForConditionalGeneration, MBart50Tokenizer

def retelling(text):
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    
    tokenizer.src_lang = "ru_RU"
    
    # Токенизация текста
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

    # Генерация пересказа
    summary_ids = model.generate(
        inputs["input_ids"], 
        max_length=100, 
        num_beams=5, 
        early_stopping=True, 
        forced_bos_token_id=tokenizer.lang_code_to_id["ru_RU"]  # Указываем язык
    )

    # Декодирование выхода
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
