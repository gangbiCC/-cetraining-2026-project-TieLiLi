class StudentManager:
    """学生成绩管理系统"""

    def __init__(self):
        """初始化空的学生列表"""
        self.students = []

    def add_student(self, id, name, score):
        """
        添加学生
        - id: 学号（字符串）
        - name: 姓名（字符串）
        - score: 成绩（整数或浮点数）
        返回: (成功, 消息)
        学号不能重复
        """
        # 检查学号是否已存在
        if self.find_by_id(id) is not None:
            return False, f"学号 {id} 已存在，添加失败"

        # 基本数据校验
        if not id or not name:
            return False, "学号和姓名不能为空"

        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            return False, "成绩必须在 0-100 之间"

        student = {"id": str(id), "name": str(name), "score": float(score)}
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

    def update_score(self, id, new_score):
        """
        修改学生成绩
        返回: (是否成功, 消息)
        """
        student = self.find_by_id(id)
        if student is None:
            return False, f"未找到学号为 {id} 的学生"

        if not isinstance(new_score, (int, float)) or new_score < 0 or new_score > 100:
            return False, "成绩必须在 0-100 之间"

        student["score"] = float(new_score)
        return True, f"学生 {student['name']} 成绩已更新为 {new_score}"

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

    def get_average(self):
        """
        计算所有学生的平均分
        返回: 浮点数，如果没有学生则返回 0.0
        """
        if not self.students:
            return 0.0

        total = sum(student["score"] for student in self.students)
        return round(total / len(self.students), 2)


# ========== 命令行交互界面 ==========
if __name__ == "__main__":
    sm = StudentManager()

    def show_menu():
        print("\n" + "=" * 40)
        print("       学生成绩管理系统")
        print("=" * 40)
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改成绩")
        print("4. 按学号查询")
        print("5. 按姓名查询")
        print("6. 显示所有学生")
        print("7. 查看平均分")
        print("0. 退出")
        print("=" * 40)

    while True:
        show_menu()
        choice = input("请选择操作: ").strip()

        if choice == "1":
            sid = input("请输入学号: ").strip()
            name = input("请输入姓名: ").strip()
            try:
                score = float(input("请输入成绩: ").strip())
            except ValueError:
                print("成绩输入无效，请输入数字")
                continue
            success, msg = sm.add_student(sid, name, score)
            print(f"[{'✓' if success else '✗'}] {msg}")

        elif choice == "2":
            sid = input("请输入要删除的学号: ").strip()
            success, msg = sm.delete_student(sid)
            print(f"[{'✓' if success else '✗'}] {msg}")

        elif choice == "3":
            sid = input("请输入学号: ").strip()
            try:
                new_score = float(input("请输入新成绩: ").strip())
            except ValueError:
                print("成绩输入无效，请输入数字")
                continue
            success, msg = sm.update_score(sid, new_score)
            print(f"[{'✓' if success else '✗'}] {msg}")

        elif choice == "4":
            sid = input("请输入学号: ").strip()
            student = sm.find_by_id(sid)
            if student:
                print(f"学号: {student['id']}, 姓名: {student['name']}, 成绩: {student['score']}")
            else:
                print(f"未找到学号为 {sid} 的学生")

        elif choice == "5":
            name = input("请输入姓名（支持模糊查询）: ").strip()
            results = sm.find_by_name(name)
            if results:
                print(f"找到 {len(results)} 条记录:")
                for s in results:
                    print(f"  学号: {s['id']}, 姓名: {s['name']}, 成绩: {s['score']}")
            else:
                print(f"未找到包含 '{name}' 的学生")

        elif choice == "6":
            all_students = sm.get_all()
            if all_students:
                print(f"共 {len(all_students)} 名学生:")
                print("-" * 30)
                print(f"{'学号':<12} {'姓名':<8} {'成绩':>6}")
                print("-" * 30)
                for s in all_students:
                    print(f"{s['id']:<12} {s['name']:<8} {s['score']:>6}")
            else:
                print("暂无学生记录")

        elif choice == "7":
            avg = sm.get_average()
            print(f"当前共 {len(sm.students)} 名学生，平均分: {avg}")

        elif choice == "0":
            print("再见！")
            break

        else:
            print("无效选项，请重新输入")