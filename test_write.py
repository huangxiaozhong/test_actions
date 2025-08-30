file_path = "test_wplus.txt"

with open(file_path, mode="w+", encoding="utf-8") as f:
    # 写入内容
    f.write("写入后立即读取
")
    
    # 将指针移动到文件开头（否则 read() 会读不到内容）
    f.seek(0)  # 关键操作！
    
    # 读取内容
    content = f.read()
    print("读取内容：", content)  # 输出：写入后立即读取

print("读写完成！")
