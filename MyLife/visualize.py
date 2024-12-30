from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

# Define language colors based on their brand colors
LANGUAGE_COLORS = {
    'Python': '#3776AB',
    'JavaScript': '#F7DF1E',
    'Java': '#007396',
    'C++': '#00599C',
    'HTML': '#E34F26',
    'CSS': '#1572B6',
    'TypeScript': '#3178C6',
    'C#': '#239120',
    'Ruby': '#CC342D',
    'Swift': '#FA7343',
    'Go': '#00ADD8',
    'Rust': '#DEA584',
    'PHP': '#777BB4',
    'R': '#276DC3',
    'Shell': '#89E051',
    'Jupyter Notebook': '#DA5B0B',
    'Vue': '#4FC08D',
    'React': '#61DAFB',
    'Kotlin': '#A97BFF',
    'Dart': '#00B4AB'
}

def get_color(language):
    """Get color for a language, with fallback to a hash-based color."""
    if language in LANGUAGE_COLORS:
        return LANGUAGE_COLORS[language]
    # Generate a color based on language name for unknown languages
    hash_val = hash(language)
    r = (hash_val & 0xFF0000) >> 16
    g = (hash_val & 0x00FF00) >> 8
    b = hash_val & 0x0000FF
    return f'#{r:02x}{g:02x}{b:02x}'

def create_language_pie(language_stats):
    """Create a pie chart of language statistics with optimized labels."""
    if not language_stats:
        return
    
    plt.figure(figsize=(14, 10))
    
    # Prepare data
    values = list(language_stats.values())
    labels = list(language_stats.keys())
    colors = [get_color(lang) for lang in labels]
    
    # Set threshold for legend entries
    threshold = 5  # percentage threshold for legend
    
    # Create labels list with empty strings for small portions
    pie_labels = ['' if v < threshold else l for l, v in zip(labels, values)]
    
    # Plot pie chart
    wedges, texts, autotexts = plt.pie(values,
                                      labels=pie_labels,
                                      colors=colors,
                                      autopct='%1.1f%%',
                                      pctdistance=0.85,
                                      startangle=90,
                                      shadow=True,
                                      wedgeprops={'edgecolor': 'white',
                                                 'linewidth': 2,
                                                 'antialiased': True})
    
    # Create legend for small slices
    small_slices = [(l, v) for l, v in zip(labels, values) if v < threshold]
    if small_slices:
        plt.legend(
            [wedges[i] for i, v in enumerate(values) if v < threshold],
            [f"{l} ({v:.1f}%)" for l, v in small_slices],
            title="Small Portions",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
    
    # Hide percentage labels for small slices
    for i, v in enumerate(values):
        if v < threshold:
            autotexts[i].set_visible(False)
    
    # Enhance text properties
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=11)
    
    plt.title("GitHub Repository Language Distribution", 
              pad=20, 
              size=14, 
              weight='bold')
    
    plt.axis('equal')
    
    plt.savefig('language_distribution.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none',
                pad_inches=0.2)
    plt.close()

def create_repo_timeline(timeline_data):
    """Create a timeline visualization of repositories with stacked bars."""
    if not timeline_data:
        return
    
    # Create figure
    plt.figure(figsize=(15, 8))
    
    # Prepare data
    periods = [group['period'] for group in timeline_data]
    
    # Generate unique colors and patterns for repositories
    all_repos = sorted(set(
        repo['name']
        for period_data in timeline_data
        for repo in period_data['repos']
    ))
    
    # Create color and pattern mapping for repos
    from matplotlib.colors import hsv_to_rgb
    repo_styles = {}
    # hatch_patterns = ['/', '\\', 'x', '+', '*', 'o', 'O', '.']
    hatch_patterns = ['/', '\\', 'x']
    
    for i, repo_name in enumerate(all_repos):
        hue = i / len(all_repos)
        color = hsv_to_rgb([hue, 0.8, 0.8])
        if i % 2 == 0 or i % 3 == 0:
            pattern = hatch_patterns[i % len(hatch_patterns)]
        else:
            pattern = ''
        repo_styles[repo_name] = {'color': color, 'hatch': pattern}
    
    # Track languages and calculate positions
    all_languages = set()
    bottom = np.zeros(len(periods))
    
    # Create stacked bars for each period
    for idx, period_data in enumerate(timeline_data):
        sorted_repos = sorted(period_data['repos'], key=lambda x: x['commits'], reverse=True)
        
        for repo in sorted_repos:
            lang = repo['language']
            commits = repo['commits']
            color = get_color(lang)
            style = repo_styles[repo['name']]
            
            # Create bar segment with color, edge and optional hatch
            bar = plt.bar(idx, commits, bottom=bottom[idx],
                         color=color, width=0.8,
                         edgecolor=style['color'],
                         linewidth=2,
                         hatch=style['hatch'] * 2,  # 双重条纹使图案更明显
                         alpha=0.9 if style['hatch'] else 1)  # 带条纹的稍微透明
            
            bottom[idx] += commits
            all_languages.add(lang)
        
        # Add total commits label on top
        total_commits = sum(repo['commits'] for repo in sorted_repos)
        plt.text(idx, bottom[idx] + 1, str(total_commits),
                ha='center', va='bottom',
                fontsize=10, weight='bold')
    
    # Customize plot
    plt.title("Monthly Commit Activity", pad=20, size=14, weight='bold')
    plt.xlabel("Time Period")
    plt.ylabel("Number of Commits")
    
    # Format x-axis
    plt.xticks(range(len(periods)), periods, rotation=45, ha='right')
    
    # Create legends
    # Language legend
    lang_legend = [
        plt.Rectangle((0,0), 1, 1, color=get_color(lang), label=lang)
        for lang in sorted(all_languages)
    ]
    lang_ax = plt.gca()
    first_legend = lang_ax.legend(handles=lang_legend,
                                 title="Languages",
                                 loc='upper left',
                                 bbox_to_anchor=(1.01, 1))
    lang_ax.add_artist(first_legend)
    
    # Repository legend with patterns
    repo_legend = [
        plt.Rectangle((0,0), 1, 1,
                     facecolor='white',
                     edgecolor=repo_styles[repo]['color'],
                     hatch=repo_styles[repo]['hatch'] * 2,
                     linewidth=2,
                     label=repo)
        for repo in all_repos
    ]
    plt.legend(handles=repo_legend,
               title="Repositories",
               loc='upper left',
               bbox_to_anchor=(1.01, 0.6))
    
    # Adjust layout
    plt.subplots_adjust(right=0.75)  # 增加右边距以适应图例
    plt.savefig('repo_timeline.png', 
                dpi=300,
                bbox_inches='tight',
                facecolor='white')
    plt.close()

def create_repo_wordcloud(timeline_data):
    """Create a word cloud visualization of repositories weighted by commit counts."""
    if not timeline_data:
        return
    
    # Calculate total commits per repository
    repo_weights = defaultdict(int)
    for period in timeline_data:
        for repo in period['repos']:
            repo_weights[repo['name']] += repo['commits']
    
    # Create word cloud
    plt.figure(figsize=(12, 8))
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        min_font_size=10,
        max_font_size=100,
        prefer_horizontal=1,
        colormap='viridis',
    ).generate_from_frequencies(repo_weights)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Repository Contribution Word Cloud", 
              pad=20, 
              size=14, 
              weight='bold')
    
    plt.savefig('repo_wordcloud.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='white')
    plt.close()
