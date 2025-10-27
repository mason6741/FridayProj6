import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sqlite3
from openai import OpenAI
import json
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import MasonsAPI_KEY

apikey = MasonsAPI_KEY.OPENAI_API_KEY

class SentimentAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Apple Vision Pro Sentiment Analysis")
        self.root.geometry("1200x800")
        
        # Initialize OpenAI client with API key from separate file
        try:
            self.client = OpenAI(api_key=MasonsAPI_KEY.OPENAI_API_KEY)
            self.api_key_loaded = True
        except:
            self.client = None
            self.api_key_loaded = False
        
        # Data storage
        self.reviews = []
        self.analysis_results = []
        
        # Create main container with tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.setup_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.setup_tab, text="Setup & Load Data")
        self.notebook.add(self.analysis_tab, text="Run Analysis")
        self.notebook.add(self.results_tab, text="Results")
        self.notebook.add(self.visualization_tab, text="Visualizations")
        
        self.create_setup_tab()
        self.create_analysis_tab()
        self.create_results_tab()
        self.create_visualization_tab()
        
    def create_setup_tab(self):
        # API Status Section
        api_frame = ttk.LabelFrame(self.setup_tab, text="OpenAI API Status", padding=10)
        api_frame.pack(fill='x', padx=10, pady=10)
        
        if self.api_key_loaded:
            status_text = "✓ API Key loaded successfully from MasonsAPI_KEY.py"
            status_color = "green"
        else:
            status_text = "✗ API Key not found. Please check MasonsAPI_KEY.py"
            status_color = "red"
        
        self.api_status_label = ttk.Label(api_frame, text=status_text, foreground=status_color)
        self.api_status_label.pack(pady=5)
        
        # Database Section
        db_frame = ttk.LabelFrame(self.setup_tab, text="Database Connection", padding=10)
        db_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(db_frame, text="Database File:").grid(row=0, column=0, sticky='w', pady=5)
        self.db_path_entry = ttk.Entry(db_frame, width=50)
        self.db_path_entry.insert(0, "feedback.db")
        self.db_path_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(db_frame, text="Browse", command=self.browse_database).grid(row=0, column=2, padx=5)
        ttk.Button(db_frame, text="Load Reviews", command=self.load_reviews).grid(row=1, column=1, pady=10)
        
        # Status Section
        status_frame = ttk.LabelFrame(self.setup_tab, text="Status", padding=10)
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, width=80)
        self.status_text.pack(fill='both', expand=True)
        
        if self.api_key_loaded:
            self.log_status("API Key loaded successfully from MasonsAPI_KEY.py")
        else:
            self.log_status("WARNING: API Key not loaded. Please check MasonsAPI_KEY.py file")
        
    def create_analysis_tab(self):
        # Control Frame
        control_frame = ttk.LabelFrame(self.analysis_tab, text="Analysis Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Run Full Analysis", 
                  command=self.run_full_analysis, 
                  style="Accent.TButton").pack(side='left', padx=5)
        ttk.Button(control_frame, text="Start Sentiment Analysis", 
                  command=self.start_sentiment_analysis).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Start Aspect Extraction", 
                  command=self.start_aspect_extraction).pack(side='left', padx=5)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(self.analysis_tab, text="Progress", padding=10)
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to analyze...")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=10)
        
        # Analysis Output
        output_frame = ttk.LabelFrame(self.analysis_tab, text="Analysis Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.analysis_output = scrolledtext.ScrolledText(output_frame, height=20, width=80)
        self.analysis_output.pack(fill='both', expand=True)
        
    def create_results_tab(self):
        # Summary Frame
        summary_frame = ttk.LabelFrame(self.results_tab, text="Summary Statistics", padding=10)
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        self.summary_text = tk.Text(summary_frame, height=8, width=80, font=('Arial', 10))
        self.summary_text.pack()
        
        # Detailed Results
        details_frame = ttk.LabelFrame(self.results_tab, text="Detailed Results", padding=10)
        details_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview for results
        columns = ('Review ID', 'Sentiment', 'Confidence', 'Key Aspects')
        self.results_tree = ttk.Treeview(details_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(details_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Export Button
        ttk.Button(self.results_tab, text="Export Results to JSON", 
                  command=self.export_results).pack(pady=10)
        
    def create_visualization_tab(self):
        # Visualization controls
        control_frame = ttk.Frame(self.visualization_tab)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Sentiment Distribution", 
                  command=self.plot_sentiment_distribution).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Aspect Frequency", 
                  command=self.plot_aspect_frequency).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Aspect Sentiment", 
                  command=self.plot_aspect_sentiment).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Generate Recommendations", 
                  command=self.generate_recommendations).pack(side='left', padx=5)
        
        # Canvas for plots
        self.viz_frame = ttk.Frame(self.visualization_tab)
        self.viz_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    def browse_database(self):
        filename = filedialog.askopenfilename(
            title="Select Database File",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.db_path_entry.delete(0, tk.END)
            self.db_path_entry.insert(0, filename)
    
    def load_reviews(self):
        db_path = self.db_path_entry.get()
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Find tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showerror("Error", "No tables found in database")
                return
            
            # Find the most likely review table
            table_name = tables[0][0]
            for table in tables:
                if 'review' in table[0].lower() or 'feedback' in table[0].lower():
                    table_name = table[0]
                    break
            
            cursor.execute(f"SELECT * FROM {table_name}")
            self.reviews = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            self.column_names = [col[1] for col in cursor.fetchall()]
            
            conn.close()
            
            self.log_status(f"Loaded {len(self.reviews)} reviews from table '{table_name}'")
            self.log_status(f"Columns: {', '.join(self.column_names)}")
            messagebox.showinfo("Success", f"Loaded {len(self.reviews)} reviews successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reviews: {str(e)}")
            self.log_status(f"Error loading reviews: {str(e)}")
    
    def analyze_sentiment(self, review_text):
        """Analyze sentiment of a single review using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Analyze the sentiment of product reviews and respond with only one word (POSITIVE, NEGATIVE, or NEUTRAL) followed by a confidence score between 0 and 1. Format: SENTIMENT CONFIDENCE"},
                    {"role": "user", "content": f"Analyze the sentiment of this Apple Vision Pro review:\n\n{review_text}"}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            result = response.choices[0].message.content.strip()
            parts = result.split()
            sentiment = parts[0].upper()
            
            # Ensure valid sentiment
            if sentiment not in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                sentiment = 'NEUTRAL'
            
            confidence = float(parts[1]) if len(parts) > 1 and parts[1].replace('.', '').isdigit() else 0.8
            
            return sentiment, confidence
        except Exception as e:
            self.log_status(f"Error in sentiment analysis: {str(e)}")
            return "NEUTRAL", 0.5
    
    def extract_aspects(self, review_text):
        """Extract specific aspects mentioned in the review"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are an expert at extracting product aspects from reviews. Extract key aspects/features mentioned in Apple Vision Pro reviews and indicate if they are mentioned positively or negatively. 
                    
Return ONLY a valid JSON array with this exact format:
[{"aspect": "display", "sentiment": "positive"}, {"aspect": "price", "sentiment": "negative"}]

Common aspects: display, comfort, price, battery, software, design, weight, apps, performance, field of view"""},
                    {"role": "user", "content": f"Extract aspects from this review:\n\n{review_text}"}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            # Clean up the response to ensure it's valid JSON
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            
            aspects = json.loads(result)
            return aspects if isinstance(aspects, list) else []
        except Exception as e:
            self.log_status(f"Error in aspect extraction: {str(e)}")
            return []
    
    def start_sentiment_analysis(self):
        if not self.reviews:
            messagebox.showwarning("Warning", "Please load reviews first")
            return
        if not self.api_key_loaded:
            messagebox.showwarning("Warning", "API key not loaded")
            return
        
        thread = threading.Thread(target=self.run_sentiment_analysis)
        thread.daemon = True
        thread.start()
    
    def run_sentiment_analysis(self):
        self.analysis_results = []
        total = len(self.reviews)
        
        for i, review in enumerate(self.reviews):
            # Find the review text column (usually last or contains 'review', 'text', 'feedback')
            review_text = str(review[-1]) if review else ""
            
            self.progress_label.config(text=f"Analyzing review {i+1}/{total}...")
            self.progress_bar['value'] = (i + 1) / total * 100
            self.root.update_idletasks()
            
            sentiment, confidence = self.analyze_sentiment(review_text)
            
            result = {
                'review_id': i + 1,
                'review_text': review_text,
                'sentiment': sentiment,
                'confidence': confidence,
                'aspects': []
            }
            self.analysis_results.append(result)
            
            self.log_analysis(f"Review {i+1}: {sentiment} (confidence: {confidence:.2f})")
        
        self.progress_label.config(text="Sentiment analysis complete!")
        messagebox.showinfo("Complete", "Sentiment analysis finished!")
        self.display_results()
    
    def start_aspect_extraction(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "Please run sentiment analysis first")
            return
        
        thread = threading.Thread(target=self.run_aspect_extraction)
        thread.daemon = True
        thread.start()
    
    def run_aspect_extraction(self):
        total = len(self.analysis_results)
        
        for i, result in enumerate(self.analysis_results):
            self.progress_label.config(text=f"Extracting aspects {i+1}/{total}...")
            self.progress_bar['value'] = (i + 1) / total * 100
            self.root.update_idletasks()
            
            aspects = self.extract_aspects(result['review_text'])
            result['aspects'] = aspects
            
            self.log_analysis(f"Review {i+1} aspects: {len(aspects)} found")
        
        self.progress_label.config(text="Aspect extraction complete!")
        messagebox.showinfo("Complete", "Aspect extraction finished!")
        self.display_results()
    
    def run_full_analysis(self):
        if not self.reviews:
            messagebox.showwarning("Warning", "Please load reviews first")
            return
        if not self.api_key_loaded:
            messagebox.showwarning("Warning", "API key not loaded")
            return
        
        thread = threading.Thread(target=self._run_full_analysis)
        thread.daemon = True
        thread.start()
    
    def _run_full_analysis(self):
        self.log_analysis("Starting full analysis...")
        self.run_sentiment_analysis()
        self.run_aspect_extraction()
        self.log_analysis("Full analysis complete!")
    
    def display_results(self):
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Display in tree
        for result in self.analysis_results:
            aspects_str = ", ".join([a.get('aspect', '') for a in result.get('aspects', [])])
            self.results_tree.insert('', 'end', values=(
                result['review_id'],
                result['sentiment'],
                f"{result['confidence']:.2f}",
                aspects_str[:50] + "..." if len(aspects_str) > 50 else aspects_str
            ))
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        if not self.analysis_results:
            return
        
        total = len(self.analysis_results)
        sentiments = [r['sentiment'] for r in self.analysis_results]
        sentiment_counts = Counter(sentiments)
        
        all_aspects = []
        for r in self.analysis_results:
            all_aspects.extend([a.get('aspect', '') for a in r.get('aspects', [])])
        
        aspect_counts = Counter(all_aspects)
        
        summary = f"""Total Reviews Analyzed: {total}

Sentiment Distribution:
  Positive: {sentiment_counts.get('POSITIVE', 0)} ({sentiment_counts.get('POSITIVE', 0)/total*100:.1f}%)
  Negative: {sentiment_counts.get('NEGATIVE', 0)} ({sentiment_counts.get('NEGATIVE', 0)/total*100:.1f}%)
  Neutral: {sentiment_counts.get('NEUTRAL', 0)} ({sentiment_counts.get('NEUTRAL', 0)/total*100:.1f}%)

Total Aspects Extracted: {len(all_aspects)}
Unique Aspects: {len(aspect_counts)}

Top 5 Most Mentioned Aspects:
"""
        for aspect, count in aspect_counts.most_common(5):
            summary += f"  {aspect}: {count} times\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
    
    def plot_sentiment_distribution(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results to visualize")
            return
        
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        sentiments = [r['sentiment'] for r in self.analysis_results]
        sentiment_counts = Counter(sentiments)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = {'POSITIVE': '#4CAF50', 'NEGATIVE': '#F44336', 'NEUTRAL': '#FFC107'}
        
        labels = list(sentiment_counts.keys())
        values = list(sentiment_counts.values())
        bar_colors = [colors.get(label, '#999999') for label in labels]
        
        ax.bar(labels, values, color=bar_colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Sentiment', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
        ax.set_title('Sentiment Distribution of Apple Vision Pro Reviews', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(values):
            ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def plot_aspect_frequency(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results to visualize")
            return
        
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        all_aspects = []
        for r in self.analysis_results:
            all_aspects.extend([a.get('aspect', '') for a in r.get('aspects', [])])
        
        aspect_counts = Counter(all_aspects)
        top_aspects = aspect_counts.most_common(10)
        
        if not top_aspects:
            messagebox.showinfo("Info", "No aspects found. Please run aspect extraction first.")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        aspects = [a[0] for a in top_aspects]
        counts = [a[1] for a in top_aspects]
        
        ax.barh(aspects, counts, color='#2196F3', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Aspect', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Most Mentioned Aspects', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        
        for i, v in enumerate(counts):
            ax.text(v + 0.3, i, str(v), va='center', fontweight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def plot_aspect_sentiment(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results to visualize")
            return
        
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        # Collect aspects with their sentiments
        aspect_sentiments = {}
        for r in self.analysis_results:
            for aspect_data in r.get('aspects', []):
                aspect = aspect_data.get('aspect', '')
                sentiment = aspect_data.get('sentiment', 'neutral')
                
                if aspect not in aspect_sentiments:
                    aspect_sentiments[aspect] = {'positive': 0, 'negative': 0, 'neutral': 0}
                
                aspect_sentiments[aspect][sentiment] = aspect_sentiments[aspect].get(sentiment, 0) + 1
        
        if not aspect_sentiments:
            messagebox.showinfo("Info", "No aspects with sentiment found.")
            return
        
        # Get top 10 most mentioned aspects
        top_aspects = sorted(aspect_sentiments.items(), 
                           key=lambda x: sum(x[1].values()), 
                           reverse=True)[:10]
        
        aspects = [a[0] for a in top_aspects]
        positives = [a[1].get('positive', 0) for a in top_aspects]
        negatives = [a[1].get('negative', 0) for a in top_aspects]
        neutrals = [a[1].get('neutral', 0) for a in top_aspects]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(aspects))
        width = 0.25
        
        ax.bar([i - width for i in x], positives, width, label='Positive', color='#4CAF50')
        ax.bar(x, negatives, width, label='Negative', color='#F44336')
        ax.bar([i + width for i in x], neutrals, width, label='Neutral', color='#FFC107')
        
        ax.set_xlabel('Aspects', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Aspect Sentiment Distribution', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(aspects, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def generate_recommendations(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results available")
            return
        
        # Analyze positive and negative aspects
        positive_aspects = []
        negative_aspects = []
        
        for r in self.analysis_results:
            for aspect in r.get('aspects', []):
                aspect_name = aspect.get('aspect', '')
                if aspect.get('sentiment') == 'positive':
                    positive_aspects.append(aspect_name)
                elif aspect.get('sentiment') == 'negative':
                    negative_aspects.append(aspect_name)
        
        pos_counts = Counter(positive_aspects)
        neg_counts = Counter(negative_aspects)
        
        # Calculate overall sentiment
        sentiments = [r['sentiment'] for r in self.analysis_results]
        sentiment_counts = Counter(sentiments)
        total = len(sentiments)
        
        recommendations = "=" * 60 + "\n"
        recommendations += "APPLE VISION PRO - INSIGHTS AND RECOMMENDATIONS\n"
        recommendations += "=" * 60 + "\n\n"
        
        recommendations += f"OVERALL SENTIMENT SUMMARY:\n"
        recommendations += f"  Total Reviews: {total}\n"
        recommendations += f"  Positive: {sentiment_counts.get('POSITIVE', 0)} ({sentiment_counts.get('POSITIVE', 0)/total*100:.1f}%)\n"
        recommendations += f"  Negative: {sentiment_counts.get('NEGATIVE', 0)} ({sentiment_counts.get('NEGATIVE', 0)/total*100:.1f}%)\n"
        recommendations += f"  Neutral: {sentiment_counts.get('NEUTRAL', 0)} ({sentiment_counts.get('NEUTRAL', 0)/total*100:.1f}%)\n\n"
        
        recommendations += "STRENGTHS (Most Appreciated Features):\n"
        recommendations += "-" * 60 + "\n"
        if pos_counts:
            for i, (aspect, count) in enumerate(pos_counts.most_common(5), 1):
                recommendations += f"  {i}. {aspect.upper()}: Mentioned positively {count} times\n"
        else:
            recommendations += "  No positive aspects identified\n"
        
        recommendations += "\nAREAS FOR IMPROVEMENT (Common Complaints):\n"
        recommendations += "-" * 60 + "\n"
        if neg_counts:
            for i, (aspect, count) in enumerate(neg_counts.most_common(5), 1):
                recommendations += f"  {i}. {aspect.upper()}: Mentioned negatively {count} times\n"
        else:
            recommendations += "  No negative aspects identified\n"
        
        recommendations += "\nACTIONABLE RECOMMENDATIONS:\n"
        recommendations += "-" * 60 + "\n"
        if neg_counts:
            for i, (aspect, count) in enumerate(neg_counts.most_common(3), 1):
                recommendations += f"  {i}. PRIORITY: Address {aspect} issues - mentioned {count} times\n"
                recommendations += f"     This is a critical area affecting customer satisfaction\n\n"
        else:
            recommendations += "  Continue maintaining current product quality\n"
        
        recommendations += "\nSTRATEGIC INSIGHTS:\n"
        recommendations += "-" * 60 + "\n"
        if pos_counts:
            top_strength = pos_counts.most_common(1)[0][0]
            recommendations += f"  • Leverage {top_strength} as a key marketing point\n"
        if neg_counts:
            top_weakness = neg_counts.most_common(1)[0][0]
            recommendations += f"  • Focus R&D efforts on improving {top_weakness}\n"
        
        recommendations += "\n" + "=" * 60 + "\n"
        
        # Display in a new window
        rec_window = tk.Toplevel(self.root)
        rec_window.title("Insights and Recommendations")
        rec_window.geometry("700x600")
        
        rec_text = scrolledtext.ScrolledText(rec_window, width=80, height=30, 
                                             font=('Courier', 10), wrap=tk.WORD)
        rec_text.pack(padx=10, pady=10, fill='both', expand=True)
        rec_text.insert(1.0, recommendations)
        rec_text.config(state='disabled')
        
        # Add export button
        ttk.Button(rec_window, text="Export Recommendations", 
                  command=lambda: self.export_recommendations(recommendations)).pack(pady=5)
    
    def export_recommendations(self, recommendations):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(recommendations)
                messagebox.showinfo("Success", "Recommendations exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_results(self):
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.analysis_results, f, indent=2)
                messagebox.showinfo("Success", "Results exported successfully!")
                self.log_status(f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def log_status(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def log_analysis(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.analysis_output.insert(tk.END, f"[{timestamp}] {message}\n")
        self.analysis_output.see(tk.END)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalysisGUI(root)
    root.mainloop()