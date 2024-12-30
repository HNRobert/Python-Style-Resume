from .github_stats import get_language_stats, get_repo_timeline
from .visualize import (create_language_pie, create_repo_timeline,
                        create_repo_wordcloud)


def list_skills(skills):
    print('\n'.join(f"{category}: {', '.join(items)}" for category, items in skills.items()))

BASIC_INFO = {'name': 'Robert He', 'age': 18, 'phone': '+86 17757341760', 'origin': 'China Mainland', 'emails': ['2567466856@qq.com', 'hnrobert@qq.com']}
EDUCATION = {'high_school': 'Haining Senior High School', 'university': 'University of Nottingham Ningbo China'}
COMPETITIONS = ['IEEExtreme18.0', 'ICPC2024', 'CSP-S']
SKILLS = {
    'Computer Basics': ['Windows, macOS, Linux Systems', 
                        'Data Structures and Algorithms', 'Build Systems', 
                        'Git, VSCode and other Basic Tools'],

    'Python': ['Data Analysis', 'NumPy & PyTorch', 
               'Windows Desktop Development', 'Flask Framework'],

    'Other Development': ['C++', 'C# & Unity', 'OpenCV',  
                          'Swift & iOS Development'],

    'Database': ['MySQL', 'SQLite'],

    'Frontend': ['HTML, CSS, JS', 'React & Vue Frameworks', 
                 'Full-stack Architecture Experience']
}
