from jsonpromax import JiebaTokenizer, default_tokenizer


def test():
    s = '你好avalonPitch hello!! ！  aadDDa'
    tokenizer = JiebaTokenizer()
    print(tokenizer)
    print(tokenizer.lcut(s))
    print(default_tokenizer())
    print(list(default_tokenizer().cut(s)))
    print(list(default_tokenizer().cut(s)))
    print(default_tokenizer().lcut(s))


if __name__ == '__main__':
    test()
