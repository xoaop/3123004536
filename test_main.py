import unittest
from main import get_text_fingerprint, calculate_similarity

class TestSimilarity(unittest.TestCase):
    def test_get_text_fingerprint(self):
        text = "这是一个测试文本"
        fp = get_text_fingerprint(text)
        self.assertIsNotNone(fp)
        # SimHash 64位，检查hash值
        self.assertIsInstance(fp.value, int)

    def test_calculate_similarity_identical(self):
        text = "相同的文本内容"
        fp1 = get_text_fingerprint(text)
        fp2 = get_text_fingerprint(text)
        similarity = calculate_similarity(fp1, fp2)
        self.assertAlmostEqual(similarity, 100.0, delta=1.0)

    def test_calculate_similarity_different(self):
        text1 = "第一篇测试文章"
        text2 = "第二篇完全不同的文章"
        fp1 = get_text_fingerprint(text1)
        fp2 = get_text_fingerprint(text2)
        similarity = calculate_similarity(fp1, fp2)
        self.assertLess(similarity, 70.0)  # 调整阈值

    def test_calculate_similarity_similar(self):
        text1 = "这是一个相似的文本"
        text2 = "这是一个相似的文章"
        fp1 = get_text_fingerprint(text1)
        fp2 = get_text_fingerprint(text2)
        similarity = calculate_similarity(fp1, fp2)
        self.assertGreater(similarity, 80.0)

    def test_empty_text(self):
        text1 = ""
        text2 = ""
        fp1 = get_text_fingerprint(text1)
        fp2 = get_text_fingerprint(text2)
        similarity = calculate_similarity(fp1, fp2)
        self.assertAlmostEqual(similarity, 100.0, delta=1.0)
        
    def test_one_empty_text(self):
        text1 = "非空文本, 包含一些内容"
        text2 = ""
        fp1 = get_text_fingerprint(text1)
        fp2 = get_text_fingerprint(text2)
        similarity = calculate_similarity(fp1, fp2)
        self.assertLess(similarity, 1.0)  # 调整阈值


if __name__ == '__main__':
    unittest.main()