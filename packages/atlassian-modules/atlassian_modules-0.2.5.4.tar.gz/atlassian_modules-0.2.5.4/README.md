The best way to interact with Atlassian Jira/Confluence API.

# Prerequisites
```python
from atlassian_modules import JiraHelper # for Jira
from atlassian_modules import  WikiHelper # for Wiki
```

# Getting Started

## Connectivity to Atlassian Jira

To initialize a connection to Jira, instantiate the `JiraHelper` class with your Jira URL, email, and API token:

```python
jira_helper = JiraHelper(JIRA_URL, EMAIL, API_TOKEN)
wiki_helper = WikiHelper(JIRA_URL, EMAIL, API_TOKEN)
```

# Atlassian Jira
## 1. Create a Jira Ticket

- You can create a new Jira ticket using the `create_ticket` method:

```python
test = jira_helper.create_ticket("XX", "Test Issue", "This is a test issue created from main.py", "Task")
print(test)
```
Parameters:
- `project_key`: The key of the project in which the ticket should be created.
- `summary`: A brief summary of the issue.
- `description`: A detailed description of the issue.
- `issue_type`: The type of the issue (e.g., "Task", "Bug", etc.).

Output:
- Preparing issue data...
- Sending request to create a ticket in project ID...
- Ticket created successfully!
- Ticket URL: `https://your-url.atlassian.net/browse/XX-1234`
- **Or error! with details!**

Return:
- test = `https://your-url.atlassian.net/browse/XX-1234`

## 2. Delete a Jira Ticket

- To delete a ticket, use the `delete_ticket` method:

```python
test = jira_helper.delete_ticket("XX-1234")
print(test)
```
Parameter:
- `ticket_key`: The unique key of the ticket you want to delete.

Output:
- Checking existence of ticket: `XX-1234`... 
- Ticket `XX-1234` exists!
- **Or error! with details!**

Return:
- `True` / `False`

## 3. Transition a Jira Ticket

- To transition a ticket to a different status, use the `transition_ticket` method:

```python
test = jira_helper.transition_ticket("XX-1234", "In Progress")
print(test)
# or
test = jira_helper.transition_ticket("XX-1234", 31)
print(test)
```

Parameters:
- `ticket_key`: The unique key of the ticket you want to transition.
- `transition_name`: The name of the transition you want to apply. This is not a case-sensitive when you apply the transition name.

Output:
- Attempting to transition ticket: `XX-1234`... 
- Using provided transition ID. 
- Successfully transitioned ticket: `XX-1234`
- **Or error! with details!**

Return:
- `True` / `False`


## 4. If exist a Jira Ticket

- To check if a ticket exist, use the `if_ticket_exist` method:

```python
test = jira_helper.if_ticket_exist("XX-1234")
print(test)
```
Parameters:
- `ticket_key`: The unique key of the ticket you want to check that exist.

Output:
- Checking existence of ticket: `XX-1234`...
- Ticket `XX-1234` exists!

Return:
- `True` / `False`

## 5. Comment on a Jira ticket

- To comment on the ticket, use the `comment_ticket` method:

```python
test = jira_helper.comment_ticket("XX-1234","test")
print(test)
```
Parameters:
- `ticket_key`: The unique key of the ticket you want to comment.
- `comment_text`: The text comment you want to post to the Jira ticket.

Output:
- Checking existence of ticket: `XX-1234`...
- Ticket `XX-1234` exists!
- Adding comment to ticket: `XX-1234`...
- Successfully added comment to ticket `XX-1234`. Comment URL: `https://your-url.atlassian.net/browse/XX-1234?focusedCommentId=5820515#comment-5820515`

Return:
- `https://your-url.atlassian.net/browse/XX-1234?focusedCommentId=5820515#comment-5820515` / `False`

## 6. Pass the JQL and get the ticket array

- To query tickets using JQL, use the `jql_ticket` method:

```python
test = jira_helper.jql_ticket('project = "PRJ" and status = Triage and type != Epic')
print(test)
# It returns all tickets

test = jira_helper.jql_ticket('project = "PRJ" and status = Triage and type != Epic', 5)
print(test)
# It returns 5 tickets
```

Parameters:
- `jql_query`: Working JQL Query.
- `max_results`: Optional. If you passed the number it will return that number of array ticket.

Output:
- Executing JQL query: `project = "PRJ" and status = Triage and type != Epic`...
- Fetched `50` tickets in this batch.
- Fetched `X` tickets in this batch.
- Total tickets found: `X`

Return:
- `['XX-1234', 'XX-1235', ...]`

# Atlassian Wiki
## 1. Creating a wiki page
- To create wiki page, use the `create_wiki_page` method:
```python
test = wiki_helper.create_wiki_page("SPACE","module test", "test data", <parent_page_id>)
print(test)
```
Parameters:
- `space_key`: Key of the Confluence space where the new page will reside.
- `title`: Title of the new page.
- `content`: Content of the new page.
- `parent_page_id`: Optional parent page ID if the new page is to be a child.
Output:
- Creating Confluence page with title `module test` in space `SPACE`, please wait...
- Page `module test` created successfully! You can view it here: `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<new_id>/module+test1`
- **Or error! with details!**

Return: 
- `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<new_id>/module+test1` / `False`

## 2. Duplicate a wiki page
- To duplicate wiki page, use the `duplicate_wiki_page` method:
```python
test = wiki_helper.duplicate_wiki_page(<source_page_id>,"SPACE","module test1", <target_parent_page_id>)
print(test)
```
Parameters:
- `source_page_id`: ID of the source Confluence page to be duplicated.
- `target_space_key`: Key of the Confluence space where the duplicated page will reside.
- `target_title`: Title of the duplicated page.
- `target_parent_page_id`: Optional parent page ID if the duplicated page is to be a child.
Output:
- Initiating duplication of page with ID `source_page_id` to space `SPACE` with title 'module test1'... 
- Successfully retrieved content from source page with ID `source_page_id`. 
- Creating Confluence page with title `module test1` in space `SPACE`, please wait... 
- Page `module test1` created successfully! You can view it here: `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<new_id>/module+test2`
- **Or error! with details!**

Return: 
- `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<new_id>/module+test1` / `False`

## 3. Create a wiki page from template
- To create a wiki page from template use the `create_page_from_template` method:
```python
test = wiki_helper.create_page_from_template(<template_id>,"SPACE","from the template1",<parent_page_id>)
print(test)
```
Parameters:
- `template_id`: ID of the Confluence template to use.
- `space_key`: Key of the Confluence space where the new page will reside.
- `title`: Title of the new page.
- `parent_page_id`: Optional parent page ID if the new page is to be a child.
Output:
- Initiating creation of page `from the template1` in space `SPACE` using template ID `template_id`...
- Successfully retrieved content from template with ID `template_id`.
- Creating the new page `from the template1` using the retrieved template content...
- Page `from the template1` successfully created in space `SPACE`.
- **Or error! with details!**
Return: 
- `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<new_id>/from+the+template1` / `False`

## 4. Move wiki page from one location to another
- To move wiki page from one location to another location without changing title use `move_wiki_page` method:
```python
test = wiki_helper.move_wiki_page(<page_id>, "SPACE", 'append' , <target_parent_page_id>)
print(test)
```
Parameters:
- `page_id`: ID of the Confluence page to be moved.
- `target_space_key`: Key of the Confluence space where the moved page will reside.
- `target_position`: Position to place the moved page relative to the parent page (e.g., `append`, `above`, `below`). Default is `append`.
- `target_parent_page_id`: Optional ID of the parent page in which the page will be moved under.
Output:
- Initiating move of page with ID `page_id`... 
- Preparing to move page `duplicate module test` to space `SPACE`. 
- Executing move operation for page `duplicate module test`... 
- Successfully moved page `duplicate module test` to space `SPACE`.
- **Or error! with details!**
Return: 
- `https://your-url.atlassian.net/wiki/spaces/SPACE/pages/<same-id>/from+the+template1` / `False`

## 4. Check if wiki page exist
- To move wiki page from one location to another location without changing title use `move_wiki_page` method:
```python
test = wiki_helper.wiki_page_exists("pages name", "SPACE")
print(test)
```
Parameters:
- `title`: Title of the Confluence wiki page.
- `space_key`: Key of the Confluence space.
Output:
- Checking if wiki page `pages name` exists in space `SPACE`...
- Wiki page `pages name` exists in space `SPACE`.
- **Or error! with details!**
Return: 
- `True` / `False`

## 5. Retrieve all child pages
- Recursively retrieve all descendant pages of a given parent page ID.
```python
test = wiki_helper.get_child_pages_recursive(<parent_id>)
print(test)
```
Parameters:
- `parent_id`: ID of the parent Confluence wiki page.
Output:
- The duration may vary depending on the number of child pages you have. Please wait...
- **Or error! with details!**
Return: 
- `[{'id': '<child_page1>', 'title': 'Daniel Cave - Offboarding', 'parentid': '<parent_id>'},...]` / `False`

## 6. Get wiki page ID
- Retrieve the ID of a Confluence wiki page by its title.
```python
test = wiki_helper.get_page_id("page - name", "SPACE")
print(test)
```
Parameters:
- `title`: Title of the Confluence wiki page.
- `space_key`: Key of the Confluence space to search in.
Output:
- Searching for page with title: `page - name` in space: `SPACE`...
- Page found! ID: `123456`
- **Or error! with details!**
Return:
- `123456` \ `False`

## 7. Replace word in wiki
- Replace all occurrences of a string in a Confluence wiki page.
```python
test = wiki_helper.replace_in_page(123456, "this", "that")
print(test)
```
Output:
- Fetching content of page ID: `123456`...
- Performing replacements...
- Page ID: 123456 updated successfully! / No occurrences of `this` found in page ID: `123456`
- **Or error! with details!**
Return:
- `True` \ `False`

## 8. Fetch tables from wiki
- Fetch all tables from a Confluence wiki page.
```python
test = wiki_helper.get_tables_from_page(123456)
print(test)
```
Output:
- Fetching content of page ID: 123456...
- Performing replacements...
- **Or error! with details!**
Return:
- {"table1": [{"FNAME": "Pavan", "MNAME": "H", "LNAME": "Bhatt"}, {"FNAME": "Pavan1", "MNAME": "H1", "LNAME": "Bhatt1"}], "table2": [{"FNAME": "Palak", "MNAME": "H", "LNAME": "Bhatt"}]}

## 9. Replace the whole wiki page
- Replace the entire Confluence wiki page with the new content
```python
test = wiki_helper.update_wiki_page(123456, 'new content')
print(test)
```
Output:
- Fetching current data of page ID: 123456...
- Updating page with new content...
- Page ID: 123456 content replaced successfully!
- **Or error! with details!**
Return:
- `True` \ `False`

# Data Privacy Note

🔒 **We respect your privacy**: This module does **not** store any of your data anywhere. It simply interacts with the Atlassian Jira API to perform the requested operations. Ensure you manage your connection details securely.

# Future Developments

In upcoming releases, I am working to add below functions...

- add story point parameter in `create_ticket` function
- `change_ticket_type` to change the issue type like from Task to Bug

Please keep an eye on the repository's release notes for the latest updates and feature rollouts.

# Release Notes

## Release 0.2.5.4 (04 Jan 2024)
- Introduced `update_wiki_page` 
  - This replaces the entire wiki page with the new content
- Updated the `README.md` - How to use `update_wiki_page`

## Release 0.2.5.3 (04 Jan 2024)
- This is just for testing purpose. not to use

## Release 0.2.5.2 (04 Jan 2024)
- Deleted due to potential bug

## Release 0.2.5.1 (04 Jan 2024)
- Deleted due to potential bug

## Release 0.2.5 (04 Jan 2024)
- Deleted due to potential bug

## Release 0.2.4 (13 Oct 2023)
- Introduced `get_tables_from_page`
  - This will help to fetch all the tables in JSON format
  - Easy to extract table! Happy days!
- Updated the `README.md` - How to use `get_tables_from_page`

## Release 0.2.3.1 (21 Sep 2023)
- Updated the `README.md` - How to use `get_page_id` and `replace_in_page`

## Release 0.2.3 (21 Sep 2023)
- Confluence functionality added 
  - Get wiki page ID `get_page_id`

## Release 0.2.2.1 (21 Sep 2023)
- Extra output suppressed from wiki class
- Confluence functionality added
  - Replace word in wiki page `replace_in_page`

## Release 0.2.2 (20 Sep 2023)
- Updated the `README.md` for better understanding
- Confluence functionality added
  - Get child pages recursively `get_child_pages_recursive`

## Release 0.2.1 (20 Sep 2023) - *Major Release*
- Updated the `README.md` for better understanding
- Fine-tuned the output to monitor the progress
- Better return format
- Confluence functionality added
    - Creating a wiki page `create_wiki_page`
    - Duplicate a wiki page `duplicate_wiki_page`
    - Create a wiki page from template `create_page_from_template`
    - Move wiki page from one location to another `move_wiki_page`
    - Check if wiki page exist `wiki_page_exists`
  
## Release 0.2 (20 Sep 2023)
- Deleted due to potential bug

## Release 0.1.4.1 (18 Sep 2023)
- Updated the `README.md` for better understanding.

## Release 0.1.4 (18 Sep 2023)
- Suppressed extra output and focused on specific output of functions for smoother integration
- Updated the `README.md` with output details
- Search a ticket `if_exist_ticket`
- Comment on a ticket `comment_ticket`
- Pass the JQL `jql_ticket`

## Release 0.1.3 (18 Sep 2023)
- Deleted due to potential bug

## Release 0.1.2.1 (16 Sep 2023)
- Updated the `README.md` format

## Release 0.1.2 (16 Sep 2023)
- Check Jira ticket exist `if_exist_ticket` added
- Updated the `README.md` format

## Release 0.1.1 (16 Sep 2023)
- Transition a Jira ticket (Can pass transition ID too) `transition_ticket`
- Modified `README.md` for clarity use of this module

## Release 0.1 (16 Sep 2023)
- Create a Jira ticket `create_ticket`
- Delete a Jira ticket `delete_ticket`
- Transition a Jira ticket (Strict to Transition Name) `transition_ticket`