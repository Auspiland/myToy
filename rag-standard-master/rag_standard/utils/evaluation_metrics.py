from typing import List, Set, Dict, Tuple
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction # type: ignore

# --- 검색 성능 지표 ---

def precision_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int) -> float:
    """
    Precision@k를 계산합니다.

    Args:
        retrieved_ids: 검색된 문서 ID 리스트 (관련도 순으로 정렬됨).
        ground_truth_ids: 정답 관련 문서 ID 집합.
        k: 고려할 상위 검색 문서의 수.

    Returns:
        Precision@k 점수.
    """
    if k == 0:
        return 0.0
    if not retrieved_ids: # 검색된 문서 없음
        return 0.0

    top_k_retrieved = retrieved_ids[:k]
    true_positives = len(set(top_k_retrieved) & ground_truth_ids)
    return true_positives / k

def recall_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int) -> float:
    """
    Recall@k를 계산합니다.

    Args:
        retrieved_ids: 검색된 문서 ID 리스트 (관련도 순으로 정렬됨).
        ground_truth_ids: 정답 관련 문서 ID 집합.
        k: 고려할 상위 검색 문서의 수.

    Returns:
        Recall@k 점수.
    """
    if not ground_truth_ids: # 정답 문서 없음
        return 0.0
    if not retrieved_ids and not ground_truth_ids: # 검색된 것도 없고, 예상된 것도 없음
        return 1.0
    if not retrieved_ids: # 검색된 것은 없으나, 정답은 존재함
        return 0.0

    top_k_retrieved = retrieved_ids[:k]
    true_positives = len(set(top_k_retrieved) & ground_truth_ids)
    return true_positives / len(ground_truth_ids)

def f1_at_k(precision_k: float, recall_k: float) -> float:
    """
    F1@k를 계산합니다.

    Args:
        precision_k: Precision@k 점수.
        recall_k: Recall@k 점수.

    Returns:
        F1@k 점수.
    """
    if precision_k + recall_k == 0:
        return 0.0
    return 2 * (precision_k * recall_k) / (precision_k + recall_k)

# --- 생성 성능 지표 ---

def calculate_rouge(predictions: List[str], references: List[List[str]]) -> List[Dict[str, Dict[str, float]]]:
    """
    예측과 참조에 대한 ROUGE 점수(R-1, R-2, R-L)를 계산합니다.

    Args:
        predictions: 생성된 답변 리스트.
        references: 정답 답변 리스트의 리스트. 각 내부 리스트는 단일 예측에 대한
                    여러 참조 답변을 포함할 수 있습니다.

    Returns:
        각각 ROUGE-1, ROUGE-2, ROUGE-L에 대한 ROUGE 점수(precision, recall, fmeasure)를
        포함하는 딕셔너리 리스트.
    """
    # NLTK 데이터 사용 가능 여부 확인 (punkt는 일부 ROUGE 버전에서 간접적으로 사용됨)
    try:
        import nltk # type: ignore
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("NLTK 'punkt' 토크나이저를 찾을 수 없습니다. 다운로드 중...")
        nltk.download('punkt', quiet=True)


    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    all_scores_typed: List[Dict[str, Dict[str, float]]] = []

    for pred, refs_for_pred in zip(predictions, references):
        current_pred_scores: Dict[str, Dict[str, float]] = {
            'rouge1': {'precision': 0.0, 'recall': 0.0, 'fmeasure': 0.0},
            'rouge2': {'precision': 0.0, 'recall': 0.0, 'fmeasure': 0.0},
            'rougeL': {'precision': 0.0, 'recall': 0.0, 'fmeasure': 0.0},
        }
        if refs_for_pred:
            # 각 참조에 대해 점수를 매기고 각 ROUGE 유형에 대해 최대 F-measure를 취합니다.
            # 이는 다중 참조를 처리하는 일반적인 방법입니다.
            
            best_scores: Dict[str, Tuple[float, float, float]] = { # P, R, F
                'rouge1': (0.0, 0.0, 0.0),
                'rouge2': (0.0, 0.0, 0.0),
                'rougeL': (0.0, 0.0, 0.0),
            }

            for ref in refs_for_pred:
                scores = scorer.score(ref, pred) # target, prediction
                for rouge_type in ['rouge1', 'rouge2', 'rougeL']:
                    if scores[rouge_type].fmeasure > best_scores[rouge_type][2]:
                        best_scores[rouge_type] = (scores[rouge_type].precision, scores[rouge_type].recall, scores[rouge_type].fmeasure)
            
            for rouge_type in ['rouge1', 'rouge2', 'rougeL']:
                current_pred_scores[rouge_type]['precision'] = best_scores[rouge_type][0]
                current_pred_scores[rouge_type]['recall'] = best_scores[rouge_type][1]
                current_pred_scores[rouge_type]['fmeasure'] = best_scores[rouge_type][2]
            
            all_scores_typed.append(current_pred_scores)
        else:
            # 참조가 없으면 기본 0점 추가
            all_scores_typed.append(current_pred_scores)
            
    return all_scores_typed


def calculate_bleu(predictions: List[str], references: List[List[str]]) -> List[float]:
    """
    예측과 참조에 대한 BLEU 점수를 계산합니다.

    Args:
        predictions: 생성된 답변 리스트 (문자열).
        references: 정답 답변 리스트의 리스트. 각 내부 리스트는
                    토큰화된 참조 답변을 포함해야 합니다.

    Returns:
        BLEU 점수 리스트.
    """
    bleu_scores: List[float] = []
    # 일반적인 스무딩 함수, method1이 많이 사용됨
    chencherry = SmoothingFunction() 

    for pred_text, refs_texts_for_pred in zip(predictions, references):
        tokenized_pred = pred_text.split() 
        tokenized_refs = [ref_text.split() for ref_text in refs_texts_for_pred]

        score: float
        if not tokenized_pred and not any(tokenized_refs): 
            score = 1.0 # 둘 다 비어있음, 어떤 의미에서는 완벽 일치
        elif not tokenized_pred or not any(tokenized_refs): 
            score = 0.0 # 하나는 비어있지만 둘 다 비어있지는 않음
        else:
            # sentence_bleu는 참조 토큰 리스트의 리스트와 가설 토큰 리스트 하나를 예상합니다.
            score = sentence_bleu(tokenized_refs, tokenized_pred, smoothing_function=chencherry.method1)
        bleu_scores.append(score)
    return bleu_scores 