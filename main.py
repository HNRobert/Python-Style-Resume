import MyLife


class HNRobert:
    def __init__(self):
        self.language_stats = MyLife.get_language_stats("HNRobert")
        self.repo_timeline = MyLife.get_repo_timeline("HNRobert")
        self.GITHUB_PROFILE = "https://github.com/HNRobert"
        MyLife.create_language_pie(self.language_stats)
    
    def print_identity(self):
        print(
            MyLife.BASIC_INFO['name'],    #  Robert He
            MyLife.BASIC_INFO['age'],     #  18
            MyLife.BASIC_INFO['origin'],  #  China Mainland
            MyLife.BASIC_INFO['phone'],   #  +86 17757341760
            MyLife.BASIC_INFO['emails']   #  2567466856@qq.com, hnrobert@qq.com
        )

    def verify_education(self):
        print("🎓 Checking education background...")
        assert 'Haining Senior High School' in MyLife.EDUCATION['high_school']
        assert 'University of Nottingham Ningbo China' in MyLife.EDUCATION['university']

    def verify_competitions(self):
        print("🏆 Validating competition experience...")
        assert 'IEEExtreme' in MyLife.COMPETITIONS[0]
        assert all(comp in MyLife.COMPETITIONS for comp in ['ICPC2024', 'CSP-S'])

    def list_skills(self):
        print("🛠️ Analyzing skill set...")
        MyLife.list_skills(MyLife.SKILLS) 
        """
        Computer Basics:     Windows, macOS, Linux Systems, 
                             Data Structures and Algorithms, Build Systems, 
                             Git, VSCode and other Basic Tools

        Python:              Data Analysis, NumPy & PyTorch, 
                             Windows Desktop Development, Flask Framework

        Other Development:   C++, C# & Unity, OpenCV, Swift & iOS Development

        Database:            MySQL, SQLite

        Frontend:            HTML, CSS, JS, React & Vue Frameworks, 
                             Full-stack Architecture Experience
        """
    
    def list_coding_experiences(self):
        print("\n👨‍💻 GitHub Repository Timeline:")
        MyLife.create_repo_timeline(self.repo_timeline)
        MyLife.create_repo_wordcloud(self.repo_timeline)

    def display_resume(self):
        self.print_identity(); self.verify_education()
        self.verify_competitions(); self.list_skills()
        self.list_coding_experiences()
        self.more()
    
    def more(self):
        print(
            "🔗 For more info about me, please visit my GitHub profile: ",
            self.GITHUB_PROFILE,  # "https://github.com/HNRobert"
            "I'm also good at: ",
            "🖇️ Teamwork", "✅ Problem-solving", "📇 Communication",
            "🎨 Designing", "🚴 Cycling", "🏸 Badminton"
        )


if __name__ == "__main__":
    resume = HNRobert()
    resume.display_resume()
