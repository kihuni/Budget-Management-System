[Live link](http://kihuni.pythonanywhere.com/)

<h1>Project Overview: Personal Budget Management System</h1>

## Introduction:
The Personal Budget Management System is a web-based application designed to help users manage their finances effectively. The system allows users to track their expenses, set budgets, analyze spending patterns, and generate reports to gain insights into their financial habits.

### Features:

User Authentication: The system provides secure user authentication using Django's built-in authentication system. Users can register, log in, and manage their accounts.

Budget Creation: Users can create budgets specifying the start and end dates, maximum spending limits, and target savings. Each budget is associated with a user account.

Expense Tracking: Users can record their expenses by specifying the title, amount, category, date, and optional details such as location and notes. Expenses are categorized to facilitate analysis.

Income Management: Users can track their income by recording the amount, source, date, and optional notes. This feature helps users understand their overall financial situation.

Transfers: The system allows users to transfer funds between budgets. Users can specify the amount, date, source budget, destination budget, and add optional notes.

Category Management: Users can create and manage categories to organize their expenses effectively. Categories can be hierarchical, allowing for a detailed breakdown of spending.

Monthly Spending Analysis: A key feature of the system is the ability to generate a monthly PDF analysis of spending. This report provides users with a summary of their expenses for the current month, categorized by spending categories.



### Implementation Details:

The system is implemented using Django, a high-level Python web framework. It utilizes Django's Model-View-Template (MVT) architecture for clean code organization and separation of concerns.

Models: The system defines several models to represent entities such as budgets, expenses, income, transfers, and categories. These models are used to store data in the database and facilitate data manipulation.

Views: Views are implemented to handle user requests and generate appropriate responses. Views interact with models to retrieve data, perform business logic, and render templates or generate PDF reports.

Templates: Templates are HTML files used to define the presentation layer of the application. They incorporate dynamic data using Django's template language and provide a user-friendly interface for interacting with the system.

Conclusion:
The Personal Budget Management System empowers users to take control of their finances by providing tools for budgeting, expense tracking, and financial analysis. With features such as monthly spending analysis, users can gain valuable insights into their spending habits and make informed financial decisions. The system aims to promote financial awareness and responsible money management among users.
