from rake_nltk import Rake

def candidate_keyword(text):
    r = Rake()
    candidate_keywords = r.extract_keywords_from_text(text)
    rank_phrases = r.get_ranked_phrases()
    return candidate_keywords, rank_phrases


# a,b = candidate_keyword("Middle market companies face a variety of new challenges daily—including ever-increasing competition. You know that optimizing efficiency is critical for increasing profitability, but where do you start At RSM, we immerse ourselves in your business so we can gain a deeper understanding of your challenges and apply a personal approach to business optimization and efficiency. This is especially important when it comes to business optimization and efficiency. We’ll work with you to identify what can be done better, faster and at less cost. Then we’ll help you map the next steps to change.When resources are properly allocated and processes are waste-free, you can capture competitive advantage and empower your organization to take the lead—now and in the future.")
# print(a,b)