import json
import os
import base64
from datetime import datetime

def generate_mistake_notebook_html(json_file_path, output_html_path, embed_images=False):
    """
    将JSON格式的错题本数据渲染为简约好看的HTML格式文件
    
    参数:
    json_file_path -- JSON文件路径
    output_html_path -- 输出HTML文件路径
    embed_images -- 是否将图片嵌入到HTML中，默认为False
    """
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取学生信息
    student_id = data.get('student_id', '')
    student_name = data.get('name', '')
    questions = data.get('questions', [])
    
    # 生成HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{student_name}的错题本</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        header {{
            background-color: #4285f4;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .student-info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        .questions-container {{
            padding: 20px;
        }}
        .question-card {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
        }}
        .question-header {{
            background-color: #f5f9ff;
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}
        .question-body {{
            padding: 15px;
        }}
        .question-content, .answer-content {{
            margin-bottom: 15px;
        }}
        .image-container {{
            margin: 10px 0;
            text-align: center;
        }}
        .image-container img {{
            max-width: 100%;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }}
        .error-reason {{
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .knowledge-points {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }}
        .knowledge-tag {{
            background-color: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #757575;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }}
        .review-info {{
            display: flex;
            align-items: center;
            font-size: 0.9em;
            color: #757575;
        }}
        .review-badge {{
            background-color: #ff5722;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 8px;
            font-size: 0.8em;
        }}
        .exam-info {{
            color: #555;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        .exam-tag {{
            display: inline-block;
            background-color: #e0f7fa;
            color: #00838f;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-top: 5px;
            margin-right: 5px;
        }}
        .section-header {{
            background-color: #f1f8ff;
            padding: 10px 15px;
            margin: 20px 0 15px 0;
            border-left: 4px solid #4285f4;
            font-weight: bold;
        }}
        h3 {{
            margin-top: 15px;
            margin-bottom: 8px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{student_name}的错题本</h1>
            <div class="student-info">
                <p>学号: {student_id}</p>
                <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </header>
        
        <div class="questions-container">
"""
    
    # 按考试分组
    exam_groups = {}
    for question in questions:
        exam_name = question.get('exam_name', '未分类')
        if exam_name not in exam_groups:
            exam_groups[exam_name] = []
        exam_groups[exam_name].append(question)
    
    # 按考试名称排序
    sorted_exam_names = sorted(exam_groups.keys())
    
    # 遍历每个考试组
    for exam_name in sorted_exam_names:
        exam_questions = exam_groups[exam_name]
        
        # 添加考试标题
        html_content += f"""
            <div class="section-header">{exam_name}</div>
"""
        
        # 遍历该考试的所有题目
        for question in exam_questions:
            question_id = question.get('question_id', '')
            error_reason = question.get('error_reason', '')
            knowledge_points = question.get('knowledge_points', [])
            review_count = question.get('review_count', 0)
            created_at = question.get('created_at', '')
            last_reviewed_at = question.get('last_reviewed_at', '尚未复习')
            
            # 题目图片路径
            question_image_path = question.get('question_image_path', '')
            student_answer_image_path = question.get('student_answer_image_path', '')
            student_answer_text = question.get('student_answer_text', '')
            std_answer_image_path = question.get('std_answer_image_path', '')
            
            # 处理图片嵌入
            question_image_tag = get_image_tag(question_image_path, "题目图片", embed_images)
            student_answer_image_tag = get_image_tag(student_answer_image_path, "我的答案", embed_images)
            std_answer_image_tag = get_image_tag(std_answer_image_path, "标准答案", embed_images)
            
            html_content += f"""
                <div class="question-card">
                    <div class="question-header">
                        <div>
                            <div class="exam-info">题号: {question_id} - 添加时间: {created_at}</div>
                            <span class="exam-tag">{exam_name}</span>
                        </div>
                        <div class="review-info">
                            <div class="review-badge">{review_count}</div>
                            <span>已复习{review_count}次 - 上次复习: {last_reviewed_at if last_reviewed_at else '尚未复习'}</span>
                        </div>
                    </div>
                    
                    <div class="question-body">
                        <div class="question-content">
                            <h3>题目</h3>
                            <div class="image-container">
                                {question_image_tag}
                            </div>
                        </div>
                        
                        <div class="answer-content">
                            <h3>我的答案</h3>
"""
            
            # 根据是否有学生答案图片来决定显示图片还是文本
            if student_answer_image_path:
                html_content += f"""
                            <div class="image-container">
                                {student_answer_image_tag}
                            </div>
"""
            elif student_answer_text:
                html_content += f"""
                            <p>{student_answer_text}</p>
"""
            
            html_content += f"""
                            <h3>标准答案</h3>
                            <div class="image-container">
                                {std_answer_image_tag}
                            </div>
"""
            
            # 错误原因
            if error_reason:
                html_content += f"""
                            <div class="error-reason">
                                <h3>错误原因</h3>
                                <p>{error_reason}</p>
                            </div>
"""
            
            # 知识点标签
            if any(knowledge_points):
                html_content += """
                            <div class="knowledge-points">
                                <h3>知识点:</h3>
"""
                for kp in knowledge_points:
                    if kp:  # 只添加非空的知识点
                        html_content += f"""
                                <span class="knowledge-tag">{kp}</span>
"""
                html_content += """
                            </div>
"""
            
            html_content += """
                        </div>
                    </div>
                </div>
"""
    
    # 添加页脚
    html_content += """
        </div>
        
        <div class="footer">
            <p>错题本 - 学习进步的阶梯</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_html_path

def get_image_tag(image_path, alt_text, embed_images=False):
    """
    根据是否嵌入图片生成不同的img标签
    
    参数:
    image_path -- 图片路径
    alt_text -- 替代文本
    embed_images -- 是否嵌入图片
    
    返回:
    img标签字符串
    """
    if not image_path:
        return f'<img src="data:image/svg+xml;charset=utf-8,%3Csvg xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 viewBox%3D%220 0 300 200%22%3E%3Crect width%3D%22300%22 height%3D%22200%22 fill%3D%22%23f3f3f3%22%3E%3C%2Frect%3E%3Ctext x%3D%22100%22 y%3D%22100%22 font-family%3D%22Arial%22 font-size%3D%2216%22 fill%3D%22%23999%22%3E无图片%3C%2Ftext%3E%3C%2Fsvg%3E" alt="{alt_text}">'
    
    if embed_images:
        try:
            # 检查文件是否存在
            if not os.path.isfile(image_path):
                return f'<img src="data:image/svg+xml;charset=utf-8,%3Csvg xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 viewBox%3D%220 0 300 200%22%3E%3Crect width%3D%22300%22 height%3D%22200%22 fill%3D%22%23f3f3f3%22%3E%3C%2Frect%3E%3Ctext x%3D%22100%22 y%3D%22100%22 font-family%3D%22Arial%22 font-size%3D%2216%22 fill%3D%22%23999%22%3E图片未找到: {os.path.basename(image_path)}%3C%2Ftext%3E%3C%2Fsvg%3E" alt="{alt_text}">'
            
            # 获取文件MIME类型
            mime_type = get_mime_type(image_path)
            
            # 读取图片并转换为base64
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # 返回嵌入式图片标签
            return f'<img src="data:{mime_type};base64,{img_data}" alt="{alt_text}">'
        except Exception as e:
            print(f"嵌入图片时出错 ({image_path}): {e}")
            return f'<img src="data:image/svg+xml;charset=utf-8,%3Csvg xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 viewBox%3D%220 0 300 200%22%3E%3Crect width%3D%22300%22 height%3D%22200%22 fill%3D%22%23f3f3f3%22%3E%3C%2Frect%3E%3Ctext x%3D%22100%22 y%3D%22100%22 font-family%3D%22Arial%22 font-size%3D%2216%22 fill%3D%22%23999%22%3E图片加载错误%3C%2Ftext%3E%3C%2Fsvg%3E" alt="{alt_text}">'
    else:
        # 返回普通图片标签
        return f'<img src="{image_path}" alt="{alt_text}" onerror="this.onerror=null; this.src=\'data:image/svg+xml;charset=utf-8,%3Csvg xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 viewBox%3D%220 0 300 200%22%3E%3Crect width%3D%22300%22 height%3D%22200%22 fill%3D%22%23f3f3f3%22%3E%3C%2Frect%3E%3Ctext x%3D%22100%22 y%3D%22100%22 font-family%3D%22Arial%22 font-size%3D%2216%22 fill%3D%22%23999%22%3E图片未找到%3C%2Ftext%3E%3C%2Fsvg%3E\'">'

def get_mime_type(file_path):
    """
    根据文件扩展名获取MIME类型
    
    参数:
    file_path -- 文件路径
    
    返回:
    MIME类型字符串
    """
    ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml'
    }
    return mime_types.get(ext, 'image/jpeg')  # 默认为JPEG

def main():
    # 示例用法
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'data.json')
    output_html = os.path.join(script_dir, 'mistake_notebook_v2.html')
    
    # 如果错题本JSON文件不存在，创建示例JSON
    if not os.path.exists(json_file):
        example_data = {
            "student_id": "001",
            "name": "颜昔酒",
            "questions": [
                {
                    "question_id": "0",
                    "question_image_path": "figs/001_20250320_10.jpg",
                    "student_answer_text": "B,C,D",
                    "std_answer_image_path": "figs/001_20250320_10_std_answer.jpg",
                    "error_reason": "不会使用vt图像解题",
                    "knowledge_points": [
                        "vt图像", "完全弹性碰撞", "动量守恒", "机械能守恒"
                    ],
                    "review_count": 0,
                    "exam_name": "2025-03-16日作业",
                    "exam_score": None,
                    "created_at": "2025-03-19 09:16:11",
                    "last_reviewed_at": None
                },
                {
                    "question_id": "1",
                    "question_image_path": "figs/001_20250321_questions/question_1.jpg",
                    "student_answer_image_path": "figs/001_20250321_student_answer/question_1.jpg",
                    "std_answer_image_path": "figs/001_20250321_std_answer/question_1.jpg",
                    "error_reason": "",
                    "knowledge_points": [
                        ""
                    ],
                    "review_count": 0,
                    "exam_name": "2025-03-20日考试",
                    "exam_score": None,
                    "created_at": "2025-03-21 09:11",
                    "last_reviewed_at": None
                }
            ]
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(example_data, f, ensure_ascii=False, indent=4)
    
    # 生成HTML错题本
    # 设置embed_images=True以嵌入图片，使HTML独立运行
    embed_images = True  # 可以根据需要修改这个参数
    generated_html = generate_mistake_notebook_html(json_file, output_html, embed_images)
    print(f"错题本已生成：{generated_html}")
    print(f"图片嵌入设置：{'已嵌入' if embed_images else '未嵌入'}")

if __name__ == "__main__":
    main()