from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import sys
import cv2

# initial
gen_numbers = np.array([[i*10, i*10+1, i*10+2, i*10+3, i*10+4, i*10+5]
                       for i in range(1000)]).reshape(-1)
# question_mark = cv2.imread('/var/www/ravenfair/static/question.png')
# matplotlib error

# os.environ['MPLCONFIGDIR'] = '/var/www/ravenfair/static'


app = Flask(__name__)

sys.path.insert(0, "/var/www/ravenfair/")

# Route to render the initial HTML template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plot', methods=['POST'])
def plot():
    # initial
    # gen_numbers = np.array([[i*10+8, i*10+9] for i in range(1000)]).reshape(-1)
    question_mark = cv2.imread('/var/www/ravenfair/static/question.png')

    # Get the filename from the form data
    configuration = request.form['configuration']
    if (configuration == '简单型'):
        configuration_dir = 'center_single'
    elif (configuration == '2x2网格型'):
        configuration_dir = 'distribute_four'
    elif (configuration == '3x3网格型'):
        configuration_dir = 'distribute_nine'
    elif (configuration == '左右型'):
        configuration_dir = 'left_center_single_right_center_single'
    elif (configuration == '上下型'):
        configuration_dir = 'up_center_single_down_center_single'
    elif (configuration == '里外型'):
        configuration_dir = 'in_center_single_out_center_single'
    elif (configuration == '内网格型'):
        configuration_dir = 'in_distribute_four_out_center_single'
    filenum_str = request.form['filename']
    filenum = int(filenum_str)
    filename = 'RAVEN_'+str(gen_numbers[filenum-1])+'_train.npz'

    # Call the plot_data function to generate the plot
    arr = plot_data(configuration_dir, filename)
    data = arr['image']
    target = arr['target']

    # # Plot the array as a heatmap
    # plt.imshow(arr, cmap='hot', interpolation='nearest')
    # plt.axis('off')

    data = data.astype(np.float32)
    plt.figure(0)
    plt.subplots_adjust(wspace=0.15, hspace=0.15,
                        left=0, right=1, bottom=0, top=1)
    for p in range(0, 8):
        plt.subplot(3, 3, p+1).imshow(data[p], 'gray')
        plt.xticks([])
        plt.yticks([])
    plt.subplot(3, 3, 9).imshow(question_mark, 'gray')
    plt.axis('off')

    # plt.savefig('/var/www/ravenfair/static/problem.jpg',
    #             dpi=70, bbox_inches='tight')
    buffer_1 = io.BytesIO()
    plt.savefig(buffer_1, dpi=70, bbox_inches='tight', format='png')
    buffer_1.seek(0)
    problem_img = base64.b64encode(buffer_1.getvalue()).decode()
    buffer_1.close()

    plt.figure(1)
    plt.subplots_adjust(wspace=0.15, hspace=0.15,
                        left=0, right=1, bottom=0, top=1)
    for p in range(0, 8):
        plt.subplot(2, 4, p+1).imshow(data[p+8], 'gray')
        plt.xticks([])
        plt.xlabel(p+1, fontsize=25)
        plt.yticks([])

    # plt.savefig('/var/www/ravenfair/static/target.jpg',
    #             dpi=70, bbox_inches='tight')
    buffer_2 = io.BytesIO()
    plt.savefig(buffer_2, dpi=70, bbox_inches='tight', format='png')
    buffer_2.seek(0)
    target_img = base64.b64encode(buffer_2.getvalue()).decode()
    buffer_2.close()

    plt.close('all')
    cv2.destroyAllWindows()
    # Convert the plot to a base64-encoded PNG image
    # buffer = io.BytesIO()

    # plt.savefig('/var/www/ravenfair/static/filename.png', format='png')
    # plt.savefig('/var/www/ravenfair/temporal/filename.png', format='png')

    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_data = base64.b64encode(buffer.getvalue()).decode()

    # Return the image data as JSON
    # return jsonify({'image_data': image_data})
    return render_template('plot.html', configuration=configuration, filename=filenum_str, target=target+1, problem_img=problem_img, target_img=target_img)

# Function to read the NumPy file and generate the plot


def plot_data(configuration_dir, filename):

    # Read the NumPy file
    # arr = np.load('./figure/'+filename)

    # arr = np.load('/var/www/ravenfair/I-RAVEN-train/' +
    arr = np.load('/var/www/ravenfair/I-RAVEN-train/' +
                  configuration_dir+'/'+filename)

    # Return the array data
    return arr


if __name__ == '__main__':
    app.run()


#  // Get the array data from the server
#     fetch('/plot_data?filename={{ filename }}')
#       .then(response => response.json())
#       .then(data => {
#         // Create a new image object
#         const img = new Image();
#         img.src = 'data:image/png;base64,' + data.image_data;

#         // Draw the image on the canvas
#         const canvas = document.getElementById('plotCanvas');
#         const ctx = canvas.getContext('2d');
#         img.onload = () => {
#           ctx.drawImage(img, 0, 0);
#         };
#       });


#   <img src="{{ url_for('temporal', filename='filename.png') }}" alt="NumPy Image">
# <img src="/var/www/ravenfair/temporal/filename.png" alt="NumPy Image">
