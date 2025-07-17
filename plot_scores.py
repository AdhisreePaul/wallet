import pandas as pd
import matplotlib.pyplot as plt

def plot_credit_scores(file_path="wallet_scores.csv"):
    """
    Reads a CSV file of wallet scores and generates a histogram of the credit_score column.
    """
    try:
        # Read the data from the CSV file
        df = pd.read_csv(file_path)

        # Check if 'credit_score' column exists
        if 'credit_score' not in df.columns:
            print(f"Error: The file '{file_path}' does not contain a 'credit_score' column.")
            return

        # Create the histogram
        plt.figure(figsize=(10, 6))
        plt.hist(df['credit_score'], bins=20, edgecolor='black', alpha=0.7)

        # Add titles and labels for clarity
        plt.title('Distribution of Credit Scores', fontsize=16)
        plt.xlabel('Credit Score', fontsize=12)
        plt.ylabel('Number of Wallets', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot to a file
        output_filename = "credit_score_distribution.png"
        plt.savefig(output_filename)
        print(f"Graph saved to {output_filename}")

        # Display the plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    plot_credit_scores() 