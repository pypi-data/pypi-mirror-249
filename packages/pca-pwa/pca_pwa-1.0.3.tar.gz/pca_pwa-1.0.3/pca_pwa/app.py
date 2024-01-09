from flask import Flask, render_template, request
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import os
import logging
from datetime import datetime
import seaborn as sns
from adjustText import adjust_text
from scipy.stats import zscore

app = Flask(__name__)


# Configure logging
""" log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.CRITICAL, format='%(asctime)s [%(levelname)s] - %(message)s') 
"""

def plot_pca(transformed_data, header, pca):
    # Set Matplotlib to use a non-interactive backend
    plt.switch_backend('agg')

    # Create a DataFrame with PCA results
    pca_data = pd.DataFrame(transformed_data[:, :2], columns=['PC1', 'PC2'])

    # Ensure that the number of samples matches the length of the header (excluding the first element)
    if len(header) == len(pca_data):
        pca_data['Sample'] = header
    else:
        # Handle the mismatch in a way suitable for your data
        # For example, you can create a generic sample name or raise an error
        pca_data['Sample'] = [f'Sample{i+1}' for i in range(len(pca_data))]

    # Identify outliers based on z-scores (you can adjust the threshold)
    z_scores = zscore(transformed_data)
    outliers_mask = np.any(np.abs(z_scores) > 2, axis=1)

    # Create a scatter plot
    plt.figure(figsize=(10, 8))
    scatter = sns.scatterplot(x='PC1', y='PC2', hue='Sample',
                              data=pca_data, palette='viridis', s=60)

    # Add labels and title
    plt.title('PCA Plot')
    plt.xlabel(f'PC1 ({round(100 * pca.explained_variance_ratio_[0], 1)}%)')
    plt.ylabel(f'PC2 ({round(100 * pca.explained_variance_ratio_[1], 1)}%)')

    # Add labels for outliers only
    texts = []
    for i, sample in enumerate(pca_data['Sample']):
        if outliers_mask[i]:
            texts.append(plt.text(pca_data['PC1'][i], pca_data['PC2'][i], sample, fontsize=8))

    # Adjust labels for better visibility with increased expand_points
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'), force_text=(0.5,0.5))

    # Move the legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Sample')

    # Adjust layout to prevent legend cutoff
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Encode the image as base64
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    return img_base64




def save_results_to_folder(result, folder_path):
    # Create a folder with a unique identifier (timestamp)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the results into the folder
    with open(os.path.join(folder_path, 'original_data.txt'), 'w') as file:
        file.write(str(result['original_data']))
    with open(os.path.join(folder_path, 'transformed_data.txt'), 'w') as file:
        file.write(str(result['transformed_data']))
    with open(os.path.join(folder_path, 'header.txt'), 'w') as file:
        file.write(str(result['header']))
    with open(os.path.join(folder_path, 'imputation_warning.txt'), 'w') as file:
        file.write(str(result['imputation_warning']))

    # Save the PCA plot image to the folder
    plot_image_path = os.path.join(folder_path, 'pca_plot.png')
    with open(plot_image_path, 'wb') as img_file:
        img_file.write(base64.b64decode(result['plot_image']))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perform_pca', methods=['POST'])
def perform_pca():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            error_message = "No file part in the request."
            return render_template('index.html', error_message=error_message)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            error_message = "No selected file."
            return render_template('index.html', error_message=error_message)

 #       try:
        # Read Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Extract data from the DataFrame
        header = df.to_numpy()[:, 0].tolist()
        data_array = df.to_numpy()[:, 1:]

        # Handle missing values based on the selected imputation method
        imputation_method = request.form.get('imputation_method')
        if imputation_method == 'custom':
            custom_value = float(request.form.get('custom_value', 0.0))
            data_array = np.array([[custom_value if isinstance(element, float) and np.isnan(element) else element for element in row] for row in data_array], dtype=object)
        elif imputation_method == 'none':
            data_array = np.array([[0.0 if isinstance(element, float) and np.isnan(element) else element for element in row] for row in data_array], dtype=object)
        else:
            imputer = SimpleImputer(strategy=imputation_method)
            data_array = imputer.fit_transform(data_array)

        # Perform PCA
        pca = PCA(n_components=2)
        transformed_data = pca.fit_transform(data_array)

        # Create a folder for saving results
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        folder_path = os.path.join('results', f'results_{timestamp}')
        
        # Prepare the result for display
        result = {
            'original_data': data_array.tolist(),
            'transformed_data': transformed_data.tolist(),
            'header': header,
            'plot_image': plot_pca(transformed_data, header, pca),
            'imputation_warning': imputation_method
        }
        
        # Save the results into the folder
        save_results_to_folder(result, folder_path)

        # Log successful execution
        logging.info(f"PCA analysis completed successfully. Results saved to: {folder_path}")

        return render_template('result.html', result=result)
#        except Exception as e:
#            error_message = f"Error processing the file: {e}"
#            logging.error(f"Error processing the file: {e}")
#            return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8082)
