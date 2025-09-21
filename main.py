import jieba
from simhash import Simhash

def get_text_fingerprint(text, top_n=20):
    """
    将中文文本转为 SimHash 指纹
    """
    
    # 中文分词
    words = jieba.lcut(text)
    
    # 可选：去除停用词（如“的”、“是”等）
    # stopwords = {'的', '了', '在', '上', '也', '和', '就', '都', '而', '及', '与', '或'}
    # words = [w for w in words if w not in stopwords and len(w) > 1]
    
    # 统计词频
    word_freq = {}
    for w in words:
        word_freq[w] = word_freq.get(w, 0) + 1
    
    # 取频率最高的 top_n 个词作为特征
    features = sorted(word_freq.items(), key=lambda x: -x[1])[:top_n]
    
    # 生成 SimHash 指纹
    simhash = Simhash(features)
    return simhash


def calculate_similarity(simhash1, simhash2):
    """
    计算两个 SimHash 的相似度（海明距离越小越相似）
    返回相似度百分比（0~100）
    """
    if (not simhash1 or not simhash2) or (simhash1.value == 0 and simhash2.value != 0) or (simhash2.value == 0 and simhash1.value != 0):
        return 0.0

    distance = simhash1.distance(simhash2)  # 海明距离
    similarity = (64 - distance) / 64 * 100  # 假设 SimHash 是 64 位
    return similarity



if __name__ == "__main__":

    # 读取命令行参数 第一个参数为原始论文路径, 第二个参数为待检测论文路径, 第三个参数为输出答案路径
    import sys
    if len(sys.argv) != 4:
        print("用法: python main.py <原始论文路径> <待检测论文路径> <输出答案路径>")
        sys.exit(1)
        
    original_file = sys.argv[1]
    check_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(original_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    with open(check_file, 'r', encoding='utf-8') as f:
        check_text = f.read()


    fp1 = get_text_fingerprint(original_text)
    fp2 = get_text_fingerprint(check_text)

    similarity = calculate_similarity(fp1, fp2)

    print(f"两篇论文的相似度为: {similarity:.2f}%")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}%\n")
    print(f"结果已写入 {output_file}")
