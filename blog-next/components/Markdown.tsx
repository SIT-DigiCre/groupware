import marked from 'marked';
import React, { useEffect } from 'react';
import highlight from 'highlightjs'
//import { cleanHtml } from '../utils/sanitize';
import DOMPurify from 'isomorphic-dompurify';

type MarkdownProps = {
  md: string;
}
marked.setOptions({
  highlight: (code, lang) => {
    return highlight.highlightAuto(code, [lang]).value;
  },
  breaks: false,
  langPrefix: 'hljs language-'
});
export const Markdown = ({ md }: MarkdownProps) => {
  const getHtml = (md: string) => {
    const config = { ADD_TAGS: ['iframe'], KEEP_CONTENT: false };
    return DOMPurify.sanitize(marked(md), config);
  }
  return (
    <div>
      <div dangerouslySetInnerHTML={{ __html: getHtml(md) }}></div>
    </div>
  );
}

