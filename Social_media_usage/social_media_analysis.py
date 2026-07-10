"""
Social Media Usage Analysis
----------------------------
Loads daily social media usage data and analyzes:
  1. Average screen time
  2. Platform comparison
  3. Weekly trend
  4. Usage pattern (posts viewed vs. time spent)
"""

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------------
try:
    data = pd.read_csv("social_media_usage.csv", parse_dates=["Date"])
except FileNotFoundError:
    raise SystemExit(
        "Could not find 'social_media_usage.csv'. "
        "Make sure it is saved in the same folder as this script."
    )

print("===== Social Media Usage Dataset =====")
print(data.to_string(index=False))

# ------------------------------------------------------------------
# 2. Average screen time
# ------------------------------------------------------------------
overall_avg = data["Time_Spent_Minutes"].mean()
print(f"\nAverage daily screen time (all platforms): {overall_avg:.1f} minutes")

# ------------------------------------------------------------------
# 3. Platform comparison
# ------------------------------------------------------------------
avg_by_platform = data.groupby("Platform")["Time_Spent_Minutes"].mean().round(1)
total_by_platform = data.groupby("Platform")["Time_Spent_Minutes"].sum()

most_used_platform = total_by_platform.idxmax()
highest_usage = total_by_platform.max()

print("\n===== Average Time Spent per Platform (minutes) =====")
print(avg_by_platform)
print("\n===== Total Time Spent per Platform (minutes) =====")
print(total_by_platform)
print(f"\nMost Used Platform: {most_used_platform} ({highest_usage} minutes total)")

# ------------------------------------------------------------------
# 4. Weekly trend
# ------------------------------------------------------------------
weekly_trend = data.groupby(pd.Grouper(key="Date", freq="W"))["Time_Spent_Minutes"].sum()
print("\n===== Weekly Time Spent (minutes) =====")
print(weekly_trend)

# ------------------------------------------------------------------
# 5. Usage pattern (posts viewed vs. time spent)
# ------------------------------------------------------------------
avg_posts_by_platform = data.groupby("Platform")["Posts_Viewed"].mean().round(1)
data["Posts_Per_Minute"] = (data["Posts_Viewed"] / data["Time_Spent_Minutes"]).round(2)
engagement_by_platform = data.groupby("Platform")["Posts_Per_Minute"].mean().round(2)

print("\n===== Average Posts Viewed per Platform =====")
print(avg_posts_by_platform)
print("\n===== Engagement Rate (posts viewed per minute) =====")
print(engagement_by_platform)

# ------------------------------------------------------------------
# 6. Visualizations
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Social Media Usage Analysis", fontsize=15, fontweight="bold")

# Platform comparison - total time
total_by_platform.sort_values(ascending=False).plot(
    kind="bar", ax=axes[0, 0], color="#4C72B0"
)
axes[0, 0].set_title("Total Time Spent by Platform")
axes[0, 0].set_xlabel("Platform")
axes[0, 0].set_ylabel("Minutes")
axes[0, 0].tick_params(axis="x", rotation=0)
axes[0, 0].grid(axis="y", linestyle="--", alpha=0.6)

# Weekly trend
weekly_trend.plot(kind="line", marker="o", ax=axes[0, 1], color="#DD8452")
axes[0, 1].set_title("Weekly Screen Time Trend")
axes[0, 1].set_xlabel("Week Ending")
axes[0, 1].set_ylabel("Total Minutes")
axes[0, 1].grid(linestyle="--", alpha=0.6)
axes[0, 1].tick_params(axis="x", rotation=20)

# Posts viewed per platform
avg_posts_by_platform.plot(kind="bar", ax=axes[1, 0], color="#55A868")
axes[1, 0].set_title("Average Posts Viewed by Platform")
axes[1, 0].set_xlabel("Platform")
axes[1, 0].set_ylabel("Avg Posts Viewed")
axes[1, 0].tick_params(axis="x", rotation=0)
axes[1, 0].grid(axis="y", linestyle="--", alpha=0.6)

# Usage pattern: time spent vs posts viewed
platform_colors = {
    "Instagram": "#E377C2",
    "Facebook": "#4C72B0",
    "WhatsApp": "#55A868",
    "YouTube": "#C44E52",
}
for platform in data["Platform"].unique():
    subset = data[data["Platform"] == platform]
    axes[1, 1].scatter(
        subset["Time_Spent_Minutes"],
        subset["Posts_Viewed"],
        label=platform,
        color=platform_colors.get(platform),
        alpha=0.8,
    )
axes[1, 1].set_title("Usage Pattern: Time Spent vs Posts Viewed")
axes[1, 1].set_xlabel("Time Spent (minutes)")
axes[1, 1].set_ylabel("Posts Viewed")
axes[1, 1].legend()
axes[1, 1].grid(linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("social_media_usage_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
