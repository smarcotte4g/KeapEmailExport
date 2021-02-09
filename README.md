# Instructions

This program will export all of the files from the given Keap
application that have been modified using the below SQL and indicated to
be email history files.

The output will be a ZIP file that contains each individual email history
file as a .html file

Make sure to add the comma separated list of email file attachment IDs
in 'file_ids.py' that is given from the SQL

## SQL

### Export Email History

#### Select the email data to save as EmailExport.csv
```sql
SELECT MailContent.FileBoxId AS 'EmailMessageId',EmailSent.ContactId,EmailSent.EmailAddress AS 'ToAddress',Mail.FromAddress,
EmailSent.DateCreated AS 'DateSent',Mail.Subject,Mail.FromName
FROM EmailSent
INNER JOIN MailContent
ON EmailSent.EmailId=MailContent.EmailId
INNER JOIN Mail
ON EmailSent.EmailId=Mail.Id WHERE MailContent.FileBoxId > 0;
```

#### Get the FileBox Id to paste into file_ids.py
```sql
SELECT Id FROM FileBox WHERE FileName LIKE 'email-%';
```

#### To Export the FileBox Ids SQLyog
```
Copy All Rows To Clipboard...
Uncheck Everything
Recheck "Lines terminated by" and add a comma
Click Ok and paste into file_ids.py
```

#### Always backup in case you jack it up
```sql
CREATE TABLE FileBox_20210204 LIKE FileBox;
INSERT INTO FileBox_20210204 SELECT * FROM FileBox;
```
#### Creates an ID to use
```sql
CREATE TABLE FileBoxEmailId_20210204 AS (SELECT Id FROM FileBox WHERE FileName LIKE 'email-%');

ALTER TABLE FileBoxEmailId_20210204 ADD INDEX Id(Id);
```

#### Changes a few columns to work with export (Anything over 100k I would run one update at a time)
```sql
UPDATE FileBox
SET FileName=CONCAT(FileName,'.html'),
Category = 'docs',
Extension = 'html',
FileBoxType = 1
WHERE Id IN (SELECT Id FROM FileBoxEmailId_20210204);
```

#### This changes everything back
```sql
UPDATE FileBox
SET FileName=LEFT(FileName,LENGTH(FileName)-5),
Category = 'email',
Extension = '',
FileBoxType = 3
WHERE Id IN (SELECT Id FROM FileBoxEmailId_20210204);
```