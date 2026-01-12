import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Santosh Kumar"

tokens = enc.encode(text)
# [25216, 3274, 0, 3673, 1308, 382, 19031, 12601, 70737]
print("Tokens", tokens)

decoded = enc.decode([25216, 3274, 0, 3673, 1308, 382, 19031, 12601, 70737])
print("Decode string is ",decoded)