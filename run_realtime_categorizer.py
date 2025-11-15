# Real-Time Perfect Transaction Categorizer
# Run this in your Jupyter notebook

import pandas as pd
from realtime_categorizer import RealTimePerfectCategorizer

# Load your preprocessed data
print("📖 Loading preprocessed transactions...")
df = pd.read_csv("preprocessed_transactions.csv")
print(f"📊 Found {len(df)} transactions to categorize")

# Initialize the real-time categorizer
print("🚀 Initializing Real-Time Perfect Categorizer...")
categorizer = RealTimePerfectCategorizer()

# Process all transactions in real-time
print("⚡ Starting real-time categorization...")
categorized_df = categorizer.categorize_batch(df)

# Save results
output_file = "realtime_categorized_perfect.csv"
categorized_df.to_csv(output_file, index=False)
print(f"💾 Results saved to: {output_file}")

# Save model for future real-time use
model_file = "realtime_perfect_model.pkl"
categorizer.save_model(model_file)
print(f"💾 Model saved to: {model_file}")

# Display comprehensive results
print(f"\n✅ Real-Time Categorization Complete!")
print(f"📊 Total Transactions Processed: {len(categorized_df)}")

# Category distribution
print(f"\n📈 Perfect Category Distribution:")
category_counts = categorized_df['Category'].value_counts()
for category, count in category_counts.items():
    percentage = (count / len(categorized_df)) * 100
    print(f"  {category:15}: {count:4d} ({percentage:5.1f}%)")

# Confidence analysis
print(f"\n🎯 Real-Time Confidence Analysis:")
avg_confidence = categorized_df['Confidence'].mean()
perfect_conf = (categorized_df['Confidence'] >= 0.95).sum()
high_conf = (categorized_df['Confidence'] >= 0.8).sum()
medium_conf = ((categorized_df['Confidence'] >= 0.6) & (categorized_df['Confidence'] < 0.8)).sum()
low_conf = (categorized_df['Confidence'] < 0.6).sum()

print(f"  Average Confidence: {avg_confidence:.3f}")
print(f"  Perfect (≥0.95): {perfect_conf}/{len(categorized_df)} ({(perfect_conf/len(categorized_df)*100):.1f}%)")
print(f"  High (0.8-0.95): {high_conf-perfect_conf}/{len(categorized_df)} ({((high_conf-perfect_conf)/len(categorized_df)*100):.1f}%)")
print(f"  Medium (0.6-0.8): {medium_conf}/{len(categorized_df)} ({(medium_conf/len(categorized_df)*100):.1f}%)")
print(f"  Low (<0.6): {low_conf}/{len(categorized_df)} ({(low_conf/len(categorized_df)*100):.1f}%)")

# Sample results by category
print(f"\n📋 Sample Perfect Classifications:")
for category in category_counts.head(10).index:
    sample = categorized_df[categorized_df['Category'] == category].head(2)
    print(f"\n  🏷️ {category}:")
    for _, row in sample.iterrows():
        desc = row['Description'][:70] + "..." if len(row['Description']) > 70 else row['Description']
        amount = row['Debit_Amount'] if row['Debit_Amount'] > 0 else row['Credit_Amount']
        print(f"    ₹{amount:8.2f} | {desc:73} | ✅ {row['Confidence']:.3f}")

# Test real-time single prediction
print(f"\n⚡ Real-Time Single Prediction Test:")
test_descriptions = [
    "UPI-ZOMATO 0000503337661345 LTD-ZOMATO-ORDER@PTYBL",
    "UPI-RAZORPAYREDBUS-REDBUS-PAYMENT@ICICI-PAYMENTTOREDBUS",
    "NEFTCR-BOFA0CN6215-EPSILONINDIADATAA-CHANDRASEKAR-SALARY",
    "UPI-AMAZON INDIA-AMAZONUPI@APL-YOUAREPAYINGFOR"
]

for desc in test_descriptions:
    category, confidence = categorizer.predict_category(desc)
    print(f"  📝 {desc[:50]}... → {category} ({confidence:.3f})")

print(f"\n🎉 Real-Time Perfect Categorization System Ready!")
print(f"📁 Output: {output_file}")
print(f"🤖 Model: {model_file}")

# Display final dataframe preview
print(f"\n📊 Final Categorized Dataset Preview:")
display(categorized_df[['Description', 'Category', 'Confidence']].head(10))