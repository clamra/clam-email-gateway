#coding=utf-8
'''
Define Datastructs for ceg
'''
import json

import lamson.encoding


class MailReq(dict):
    '''
    MailReq represent an incoming email
    >>> mr = {'recipient' : u'r@example.com',
    ...       'sender' : u's@sender.com',
    ...       'from' : u'sender@sender.com',
    ...       'subject' : u'Interesting topic 是吗?',
    ...       'body-plain' : u'Hi James\\n 很高兴认识你?',
    ...       'body-html' : u'<p>Hi James</p> <p>很高兴认识你?</p>',
    ...       'attachments' : [{'name' : u"1.jpg", 'content' : "jpgaaaaaaaaaaa"}],
    ...       'message-headers' : [('X-Header-Mail-Agent', u"Clam")]
    ... }
    >>> mr = MailReq(mr)
    >>> payload, files = mr.to_http_payload()
    >>> expected_payload = [
    ...     ('X-Header-Mail-Agent', u'Clam'),
    ...     ('attachment-count', 1),
    ...     ('body-html', u'<p>Hi James</p> <p>很高兴认识你?</p>'),
    ...     ('body-plain', u'Hi James\\n 很高兴认识你?'),
    ...     ('from', u'sender@sender.com'),
    ...     ('message-headers', '[["X-Header-Mail-Agent", "Clam"]]'),
    ...     ('recipient', u'r@example.com'),
    ...     ('sender', u's@sender.com'),
    ...     ('subject', u'Interesting topic 是吗?'),
    ... ]
    >>> sorted(payload) == sorted(expected_payload)
    True
    >>> expected_files = [
    ...     (u"1.jpg", "jpgaaaaaaaaaaa")
    ... ]
    >>> files == expected_files
    True
    '''

    fields = [
        ('recipient', unicode),
        ('sender', unicode),
        ('from', unicode),
        ('subject', unicode),
        ('body-plain', unicode),
        ('body-html', unicode),
        ('attachments', list),
        ('message-headers', list)
    ]

    @classmethod
    def from_string(cls, data):
        mail = lamson.encoding.from_string(data)
        data = {}
        data['message-headers'] = mail.headers.items()
        if 'to' in mail:
            data['recipient'] = mail['to']
        if 'from' in mail:
            data['from'] = mail['from']
        if 'subject' in mail:
            data['subject'] = mail['subject']
        data['attachments'] = []
        #for multipart email
        if mail.parts:
            for part in mail.parts:
                ctype, ctype_params = part.content_encoding['Content-Type']
                if ctype == 'text/plain':
                    data['body-plain'] = part.body
                elif ctype == 'text/html':
                    data['body-plain'] = part.body
                else:
                    data['attachments'].append({
                        'name' : ctype_params.get('name'),
                        'content' : part.body,
                        'content-type' : ctype
                    })
        else:
            data['body-plain'] = mail.body
        return cls(data)

    def to_http_payload(self):
        payload = []
        files = []
        for field,_ in self.fields:
            if field == 'attachments':
                payload.append(('attachment-count', len(self.get('attachments', []))))
                for att in self.get('attachments', []):
                    files.append((att['name'], att['content']))
            elif field == 'message-headers':
                payload.append(('message-headers', json.dumps(self.get('message-headers', []))))
                for k,v in self.get('message-headers', []):
                    payload.append((k, v))
            else:
                payload.append((field, self.get(field, u'')))
        return payload, files

class Attachment(dict):
    fields = [
        ('cid', int),
        ('name', unicode),
        ('content', str),
    ]
