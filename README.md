<h1>File Metadata Viewer Documentation</h1>

<h2>Introduction</h2>

<p>The File Metadata Viewer is a graphical user interface (GUI) application built in Python using the Tkinter library. It provides a user-friendly way to view metadata information for files in a specified directory.</p>

<h2>Installation</h2>

<ol>
    <li>Ensure you have Python installed on your system. If not, download and install it from <a href="https://www.python.org/">Python's official website</a>.</li>
    <li>Clone or download the project repository from <a href="https://github.com/gartonq/MetaForensic-Explorer">GitHub</a>.</li>
    <li>Install the required Python libraries using one of the following methods:
        <ul>
            <li>Using <code>pip install</code>:</li>
        </ul>
  <pre>
  <code>pip install ttkthemes filetype python-magic pyexifinfo</code></pre>

  <ul>
            <li>Using a requirements file:</li>
        </ul>

  <pre><code>pip install -r requirements.txt</code></pre>

  Ensure that you run these commands in the directory where your project files are located.
    </li>
</ol>


<h2>Usage</h2>

<h3>Running the Application</h3>

<p>Execute the <code>main.py</code> file to launch the File Metadata Viewer GUI.</p>

<pre>
    <code>python main.py</code>
</pre>

<h3>GUI Overview</h3>

<ul>
    <li><strong>Choose directory:</strong> Select a directory using the provided entry and button.</li>
    <li><strong>Choose file:</strong> Choose a specific file using the entry and button.</li>
    <li><strong>Listbox:</strong> Displays information about files and directories based on selected actions.</li>
    <li><strong>Reset button:</strong> Clears selected directory, file, and Listbox contents.</li>
    <li><strong>Mode toggle button:</strong> Switches between Light Mode and Dark Mode.</li>
</ul>

<h3>Functionality</h3>

<h4>Tree View</h4>

<p>Click the "Tree" button to display a hierarchical tree view of the selected directory and file details.</p>

<h4>File Size</h4>

<p>Click the "File Size" button to display file sizes for the selected file or the entire directory.</p>

<h4>Metadata (Exiftool)</h4>

<p>Click the "Metadata" button to display metadata using the pyexifinfo (exiftool wraper) library.</p>

<h4>File Extension</h4>

<p>Click the "File Extension" button to display file types using both the <code>filetype</code> and <code>magic</code> libraries.</p>

<h4>Strings</h4>

<p>Click the "Strings" button to display the content of a selected file.</p>

<h4>Save</h4>

<p>Click the "Save" button to save data from the Listbox or Treeview to a CSV or text file.</p>

<h2>Classes</h2>

<h3><code>GraphicApp</code></h3>

<p>The <code>GraphicApp</code> class represents the main application window and utilizes the <code>AppEngine</code> class for backend logic.</p>

<h3><code>AppEngine</code></h3>

<p>The <code>AppEngine</code> class contains the backend logic for the File Metadata Viewer application.</p>

<h2>Notes</h2>

<ul>
    <li>This application relies on various libraries, including <code>ttkthemes</code>, <code>filetype</code>, <code>python-magic</code>, <code>pyexifinfo</code>, and standard Python libraries such as <code>tkinter</code>, <code>os</code>, and <code>csv</code>.</li>
    <li>Make sure to handle any potential errors, such as file not found or permission issues, when using the application.</li>
    <li>If you will have any problems with magic library try <code>pip install --upgrade python-magic</code> </li>
</ul>

<p>Now you are ready to explore and analyze file metadata using the File Metadata Viewer!</p>
