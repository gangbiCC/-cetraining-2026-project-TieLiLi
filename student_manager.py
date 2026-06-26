import csv
import os


class StudentManager:
    """学生成绩管理系统（支持三科成绩：Python、Java、C++）"""

    # CSV 列名
    FIELDS = ["id", "name", "python", "java", "cpp"]

    def __init__(self):
        """初始化空的学生列表"""
        self.students = []

    def add_student(self, id, name, python, java, cpp):
        """
        添加学生
        - id: 学号（字符串）
        - name: 姓名（字符串）
        - python: Python成绩（整数或浮点数）
        - java: Java成绩（整数或浮点数）
        - cpp: C++成绩（整数或浮点数）
        返回: (成功, 消息)
        学号不能重复
        """
        # 检查学号是否已存在
        if self.find_by_id(id) is not None:
            return False, f"学号 {id} 已存在，添加失败"

        # 基本数据校验
        if not id or not name:
            return False, "学号和姓名不能为空"

        # 校验三科成绩
        for subject, score in [("Python", python), ("Java", java), ("C++", cpp)]:
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                return False, f"{subject}成绩必须在 0-100 之间"

        student = {
            "id": str(id),
            "name": str(name),
            "python": float(python),
            "java": float(java),
            "cpp": float(cpp),
        }
        self.students.append(student)
        return True, f"学生 {name} 添加成功"

    def delete_student(self, id):
        """
        按学号删除学生
        返回: (是否成功, 消息)
        """
        for i, student in enumerate(self.students):
            if student["id"] == str(id):
                name = student["name"]
                self.students.pop(i)
                return True, f"学生 {name}（学号: {id}）已删除"
        return False, f"未找到学号为 {id} 的学生"

    def update_score(self, id, subject, new_score):
        """
        修改指定科目成绩
        - id: 学号
        - subject: 科目名（"python" / "java" / "cpp"）
        - new_score: 新成绩
        返回: (是否成功, 消息)
        """
        valid_subjects = {"python": "Python", "java": "Java", "cpp": "C++"}

        if subject not in valid_subjects:
            return False, f"无效科目: {subject}，可选: python/java/cpp"

        student = self.find_by_id(id)
        if student is None:
            return False, f"未找到学号为 {id} 的学生"

        if not isinstance(new_score, (int, float)) or new_score < 0 or new_score > 100:
            return False, "成绩必须在 0-100 之间"

        student[subject] = float(new_score)
        return True, f"学生 {student['name']} 的{valid_subjects[subject]}成绩已更新为 {new_score}"

    def find_by_id(self, id):
        """
        按学号精确查询
        返回: 学生字典 或 None
        """
        for student in self.students:
            if student["id"] == str(id):
                return student
        return None

    def find_by_name(self, name):
        """
        按姓名模糊查询（支持部分匹配）
        返回: 匹配的学生列表
        """
        if not name:
            return []

        result = []
        for student in self.students:
            if str(name).lower() in student["name"].lower():
                result.append(student)
        return result

    def get_all(self):
        """
        获取所有学生列表
        返回: 学生列表
        """
        return self.students

    def get_average(self, subject=None):
        """
        计算平均分
        - subject: 指定科目 ("python"/"java"/"cpp") 或 None（计算总平均）
        返回: 浮点数，如果没有学生则返回 0.0
        """
        if not self.students:
            return 0.0

        if subject:
            total = sum(student[subject] for student in self.students)
        else:
            total = sum(
                student["python"] + student["java"] + student["cpp"]
                for student in self.students
            ) / 3

        return round(total / len(self.students), 2)

    def get_rank(self, subject=None):
        """
        获取排名
        - subject: 指定按某科排名，None 则按总分排名
        返回: 排序后的学生列表（降序）
        """
        if subject:
            return sorted(self.students, key=lambda s: s[subject], reverse=True)
        else:
            return sorted(
                self.students,
                key=lambda s: s["python"] + s["java"] + s["cpp"],
                reverse=True,
            )

    # ==================== CSV 导入导出 ====================

    def export_to_csv(self, filename):
        """
        将学生数据导出为CSV文件
        包含字段：学号、姓名、Python成绩、Java成绩、C++成绩
        返回: (是否成功, 消息)
        """
        try:
            with open(filename, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS)
                writer.writeheader()
                for student in self.students:
                    writer.writerow({
                        "id": student["id"],
                        "name": student["name"],
                        "python": student["python"],
                        "java": student["java"],
                        "cpp": student["cpp"],
                    })
            return True, f"成功导出 {len(self.students)} 条记录到 {filename}"
        except PermissionError:
            return False, f"没有权限写入文件 {filename}"
        except Exception as e:
            return False, f"导出失败: {e}"

    def import_from_csv(self, filename, on_duplicate="skip"):
        """
        从CSV文件导入学生数据
        - filename: CSV文件路径
        - on_duplicate: 遇到重复学号时的处理方式
            "skip"  - 跳过（默认）
            "update" - 覆盖更新
        返回: (是否成功, 消息, 统计信息)
        """
        if not os.path.exists(filename):
            return False, f"文件不存在: {filename}", {}

        try:
            with open(filename, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                # 校验CSV表头
                missing = set(self.FIELDS) - set(reader.fieldnames or [])
                if missing:
                    return False, f"CSV文件缺少字段: {', '.join(missing)}", {}

                added, updated, skipped, errors = 0, 0, 0, 0

                for row_num, row in enumerate(reader, start=2):
                    sid = row["id"].strip()
                    name = row["name"].strip()

                    if not sid or not name:
                        errors += 1
                        continue

                    try:
                        python = float(row["python"])
                        java = float(row["java"])
                        cpp = float(row["cpp"])
                    except (ValueError, KeyError):
                        errors += 1
                        continue

                    existing = self.find_by_id(sid)

                    if existing:
                        if on_duplicate == "update":
                            existing["name"] = name
                            existing["python"] = python
                            existing["java"] = java
                            existing["cpp"] = cpp
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        self.students.append({
                            "id": sid,
                            "name": name,
                            "python": python,
                            "java": java,
                            "cpp": cpp,
                        })
                        added += 1

            stats = {"added": added, "updated": updated, "skipped": skipped, "errors": errors}
            return True, f"导入完成: 新增{added} 更新{updated} 跳过{skipped} 错误{errors}", stats

        except PermissionError:
            return False, f"没有权限读取文件 {filename}", {}
        except Exception as e:
            return False, f"导入失败: {e}", {}


# ========== 测试代码 ==========
if __name__ == "__main__":
    print("=" * 50)
    print("  学生成绩管理系统 — CSV 导入导出测试")
    print("=" * 50)

    sm = StudentManager()

    # 1. 添加测试数据
    print("\n--- 1. 添加测试学生 ---")
    sm.add_student("2024001", "张三", 85, 90, 78)
    sm.add_student("2024002", "李四", 92, 88, 95)
    sm.add_student("2024003", "王五", 76, 82, 80)
    sm.add_student("2024004", "赵六", 90, 95, 93)

    for s in sm.get_all():
        print(f"  {s['id']} {s['name']} | Python:{s['python']} Java:{s['java']} C++:{s['cpp']}")

    # 2. 导出为CSV
    print("\n--- 2. 导出到 CSV ---")
    ok, msg = sm.export_to_csv("students_export.csv")
    print(f"  [{'✓' if ok else '✗'}] {msg}")

    # 3. 验证CSV内容
    print("\n--- 3. 验证 CSV 文件内容 ---")
    if os.path.exists("students_export.csv"):
        with open("students_export.csv", "r", encoding="utf-8-sig") as f:
            print(f.read())

    # 4. 清空并重新导入
    print("\n--- 4. 清空数据，从 CSV 重新导入 ---")
    sm2 = StudentManager()
    ok, msg, stats = sm2.import_from_csv("students_export.csv")
    print(f"  [{'✓' if ok else '✗'}] {msg}")
    assert len(sm2.get_all()) == 4, "导入数量错误！"

    # 5. 测试重复学号处理
    print("\n--- 5. 测试重复学号（skip） ---")
    ok, msg, stats = sm2.import_from_csv("students_export.csv", on_duplicate="skip")
    print(f"  [{'✓' if ok else '✗'}] {msg}  (新增:{stats['added']} 跳过:{stats['skipped']})")
    assert stats["skipped"] == 4, "应跳过全部4条！"

    print("\n--- 6. 测试重复学号（update） ---")
    ok, msg, stats = sm2.import_from_csv("students_export.csv", on_duplicate="update")
    print(f"  [{'✓' if ok else '✗'}] {msg}  (更新:{stats['updated']} 跳过:{stats['skipped']})")
    assert stats["updated"] == 4, "应更新全部4条！"

    # 6. 测试文件不存在
    print("\n--- 7. 测试文件不存在 ---")
    ok, msg, stats = sm2.import_from_csv("nonexistent.csv")
    print(f"  [{'✗'}] {msg}")

    # 7. 排名
    print("\n--- 8. 总分排名 ---")
    for rank, s in enumerate(sm2.get_rank(), 1):
        total = s["python"] + s["java"] + s["cpp"]
        print(f"  {rank}. {s['id']} {s['name']} 总分:{total:.1f} (Python:{s['python']} Java:{s['java']} C++:{s['cpp']})")

    # 8. 平均分
    print(f"\n--- 9. 平均分 ---")
    print(f"  总平均分: {sm2.get_average():.2f}")
    print(f"  Python平均: {sm2.get_average('python'):.2f}")
    print(f"  Java平均:   {sm2.get_average('java'):.2f}")
    print(f"  C++平均:    {sm2.get_average('cpp'):.2f}")

    # 9. 清理测试文件
    os.remove("students_export.csv")
    print(f"\n{'=' * 50}")
    print("  所有测试通过！")
    print("=" * 50)