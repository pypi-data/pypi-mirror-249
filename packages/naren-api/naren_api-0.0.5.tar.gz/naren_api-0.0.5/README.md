## ::: Base Skeleton for Data-Science Projects :::

### Steps to run this Bare-Bones Template: 
**{Note}**: Operates exclusively within the 'Git Bash' environment.

1. Run below command 
```bash
python template.py
```
-|- Upon initiating the project, remove the 'temp.log' temporary log file.

-|- Include modules or packages in the requirements.txt file according to the specific requirements of your project.

-|- Modify the 'setup.cfg' and 'setup.py' files according to the specific requirements(project_name_description) of the project.

2. Run below command
```bash
bash init_setup.sh
```

**To activate environment in bash:**
```bash
source ~/Anaconda3/etc/profile.d/conda.sh
conda activate venv/
```

3. Run below command (optional)
```bash
pytest -v
tox
```
<br>

---

The base skeleton for a data science project typically includes the following components:

1. **Project Structure:**
   - Create a well-organized directory structure for your project.
   - Divide folders for data, code, documentation, and models.

2. **Data Collection and Exploration:**
   - Gather relevant data from various sources.
   - Explore and understand the data through descriptive statistics and visualizations.

3. **Data Cleaning and Preprocessing:**
   - Handle missing values, outliers, and inconsistencies in the data.
   - Transform and preprocess the data for analysis.

4. **Feature Engineering:**
   - Create new features or transform existing ones to improve model performance.

5. **Model Building:**
   - Select appropriate algorithms based on the problem.
   - Split the data into training and testing sets.
   - Train and evaluate models using appropriate metrics.

6. **Model Deployment:**
   - Deploy the chosen model for real-world use if applicable.

7. **Documentation:**
   - Provide clear documentation for your code, including comments and a README file.

8. **Version Control:**
   - Use version control (e.g., Git) to track changes and collaborate with others.

9. **Testing and Validation:**
   - Implement testing procedures to validate the correctness of your code.

10. **Visualization and Reporting:**
    - Create visualizations to communicate insights.
    - Prepare a report summarizing the findings and methodology.

This basic structure ensures a systematic and reproducible approach to data science projects.