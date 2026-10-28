# v2 EDA Takeaways

Source: `data/processed/v2/merged.csv` (5,455 subscribers). Every chart has the same one-line takeaway as its caption.

### Histogram of Avg Logins Per Month
![Histogram of Avg Logins Per Month](hist_avg_logins.png)
Right-skewed: median 6 logins/month, with 416 subscribers at a genuine zero.

### Histogram of Avg Session Minutes
![Histogram of Avg Session Minutes](hist_avg_session_minutes.png)
Session minutes cluster around 22 minutes/month with a mild right tail to 108.

### Histogram of Books Accessed
![Histogram of Books Accessed](hist_books_accessed.png)
Books accessed is right-skewed: median 9, long tail to 59 books.

### Histogram of Days Since Last Activity (clipped at 365)
![Histogram of Days Since Last Activity (clipped at 365)](hist_days_since_activity.png)
Highly skewed — median 17 days; 11 rows above the 365-day capture cap are shown in the last bin.

### Histogram of Subscription Tenure (Months)
![Histogram of Subscription Tenure (Months)](hist_subscription_tenure.png)
Tenure is near-uniform from 1 to 72 months, median 16.

### Correlation Heatmap — Engagement Metrics + Tenure
![Correlation Heatmap — Engagement Metrics + Tenure](heatmap_engagement_corr.png)
Only logins vs books accessed is strong (r=0.90, n=5280 complete rows); tenure barely correlates with anything.

### Genre Preference of Subscribers
![Genre Preference of Subscribers](bar_genre_preference.png)
Fiction is the largest preference (1,081 subscribers, 20%), with 54 rows carrying no stated genre (Unknown).

### Active vs Inactive vs Churned
![Active vs Inactive vs Churned](pie_status.png)
Of the 5,422 classified subscribers, 55.2% are Active and 16.6% Churned (33 Unclassified rows are not in this pie).

### Mean Logins, Session Minutes, Books Accessed and Tenure by Status
![Mean Logins, Session Minutes, Books Accessed and Tenure by Status](bar_means_by_status.png)
Active subscribers lead on behaviour (mean 11.7 logins, 16.2 books) but tenure is almost flat across statuses, so behaviour — not how long they have been subscribed — separates the groups.

### Correlation redundancy check
- **Avg Logins Per Month vs Books Accessed**: r = 0.898 (>0.8). Both measure usage frequency, so both in one score would double-count that behaviour.

(No weights or thresholds chosen here — pairs are reported only.)
