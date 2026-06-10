import re

import snowballstemmer

# Türkçe gövdeleyici (stemmer). Kelimeleri köklerine indirgeyerek
# çekim eklerinden bağımsız eşleştirme yapmayı sağlar.
_stemmer = snowballstemmer.stemmer("turkish")

# Türkçe sesli harfler (geçerlilik kontrolü için kullanılır)
_VOWELS = set("aeıioöuü")


def _tokenize(text: str):
    """Metni küçük harfli kelimelere ayırır (noktalama temizlenir)."""
    return re.findall(r"[a-zçğıöşü0-9]+", text.lower())


def _stem(word: str):
    return _stemmer.stemWord(word.lower())


def _stem_set(text: str):
    """Cümledeki tüm kelimelerin gövdelerinden oluşan küme."""
    return {_stem(tok) for tok in _tokenize(text)}


def split_sentences(text: str):
    text = text.strip()
    sentences = re.split(r"[.\n!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def _count_matches(sentence_lower: str, sentence_stems: set, keywords):
    """
    Anahtar kelime eşleşmelerini sayar.
    - Tek kelimelik anahtarlar: gövde (stem) eşitliğiyle karşılaştırılır
      (örn. 'olmalıdır', 'olmalı', 'olmaktadır' aynı köke iner).
    - Çok kelimelik anahtarlar (öbekler): alt-dizi olarak aranır.
    """
    count = 0
    for kw in keywords:
        if " " in kw:
            if kw in sentence_lower:
                count += 1
        else:
            if _stem(kw) in sentence_stems:
                count += 1
    return count


def classify_requirement(sentence: str):
    sentence_lower = sentence.lower()
    sentence_stems = _stem_set(sentence)

    nfr_keywords = [
        "hızlı", "güvenli", "performans", "kullanılabilir", "kullanılabilirlik",
        "ölçeklenebilir", "erişilebilir", "erişilebilirlik", "kararlı", "stabil",
        "dayanıklı", "uyumlu", "uyumluluk", "gizlilik", "mahremiyet", "verimli",
        "verimlilik", "response time", "yanıt süresi", "tepki süresi", "availability",
        "uptime", "latency", "throughput", "reliable", "secure", "fast", "performance",
        "scalable", "usability", "accessibility", "privacy", "maintainable",
        "maintainability", "fault tolerant", "interoperability",
    ]

    constraint_keywords = [
        "zorunlu", "zorundadır", "olmalıdır", "gereklidir", "gerekir",
        "uygun olmalıdır", "must", "required", "shall", "has to", "kvkk", "gdpr",
        "iso", "mevzuat", "yasal", "regülasyon", "standarda uygun",
        "standartlara uygun", "uyumluluk gereği", "yalnızca", "sadece", "en az",
        "en fazla",
    ]

    fr_keywords = [
        "giriş yap", "kayıt ol", "listele", "görüntüle", "oluştur", "sil",
        "güncelle", "ekle", "indir", "yükle", "ara", "filtrele", "raporla",
        "hesapla", "doğrula", "gönder", "kaydet", "giriş yapabil", "çıkış yapabil",
        "ödeme yap", "şifre sıfırla", "giriş yapabilmelidir", "görüntüleyebilmelidir",
        "oluşturabilmelidir", "güncelleyebilmelidir", "silebilmelidir",
        "ekleyebilmelidir", "yapabilmelidir", "can log in", "can view", "can create",
        "can update", "can delete", "can upload", "can download", "can search",
        "can filter",
    ]

    nfr_score = _count_matches(sentence_lower, sentence_stems, nfr_keywords)
    constraint_score = _count_matches(sentence_lower, sentence_stems, constraint_keywords)
    fr_score = _count_matches(sentence_lower, sentence_stems, fr_keywords)

    if constraint_score > 0:
        return "Non-Functional Requirement"
    if nfr_score > 0:
        return "Non-Functional Requirement"
    if fr_score > 0:
        return "Functional Requirement"
    return "Functional Requirement"


def detect_ambiguity(sentence: str):
    ambiguity_words = [
        "hızlı", "kolay", "güvenli", "kullanıcı dostu", "etkili", "iyi", "uygun",
        "optimal", "modern", "esnek", "başarılı", "güçlü", "yüksek performanslı",
        "sorunsuz", "stabil", "kararlı", "anlaşılır", "basit", "makul", "yeterli",
        "minimum", "maksimum", "short", "easy", "user-friendly", "efficient",
        "appropriate", "good", "robust",
    ]

    sentence_lower = sentence.lower()
    sentence_stems = _stem_set(sentence)

    found = []
    for word in ambiguity_words:
        if " " in word or "-" in word:
            if word in sentence_lower:
                found.append(word)
        else:
            if _stem(word) in sentence_stems:
                found.append(word)
    return found


QUALITY_SCORES = {"İyi": 100, "Orta": 65, "Düşük": 35}


def evaluate_quality(sentence: str, ambiguity_words: list):
    issues = []
    suggestions = []

    if ambiguity_words:
        issues.append("Muğlak ifade içeriyor.")
        suggestions.append("Daha ölçülebilir ve açık bir ifade kullanılması önerilir.")

    if len(sentence.split()) < 3:
        issues.append("Cümle çok kısa olabilir.")
        suggestions.append("Gereksinim daha açıklayıcı biçimde yazılabilir.")

    # "ve" bağlacını yalnızca ayrı bir kelime olarak ara.
    if re.search(r"\bve\b", sentence.lower()) and len(sentence.split()) > 8:
        issues.append("Birden fazla gereksinim tek cümlede ifade edilmiş olabilir.")
        suggestions.append("Gereksinimler ayrı cümlelere bölünebilir.")

    if not issues:
        quality = "İyi"
        suggestion = "Sorun tespit edilmedi."
    elif len(issues) == 1:
        quality = "Orta"
        suggestion = suggestions[0]
    else:
        quality = "Düşük"
        suggestion = " ; ".join(suggestions)

    return quality, issues, suggestion, QUALITY_SCORES[quality]


def analyze_requirements(text: str):
    sentences = split_sentences(text)
    results = []
    for sentence in sentences:
        req_type = classify_requirement(sentence)
        ambiguity_words = detect_ambiguity(sentence)
        quality, issues, suggestion, quality_score = evaluate_quality(sentence, ambiguity_words)
        results.append(
            {
                "sentence": sentence,
                "type": req_type,
                "ambiguity_words": ambiguity_words,
                "quality": quality,
                "quality_score": quality_score,
                "issues": issues,
                "suggestion": suggestion,
            }
        )
    return results
