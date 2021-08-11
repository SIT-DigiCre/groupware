import marked from 'marked';
import { useEffect } from 'react';
import highlight from 'highlightjs'
//import { cleanHtml } from '../utils/sanitize';
import DOMPurify from 'isomorphic-dompurify';

type MarkdownProps = {
  md: string;
}

export const Markdown = ({md}:MarkdownProps) => {
  useEffect(() => {
    marked.setOptions({
      highlight: (code, lang) => {
        return highlight.highlightAuto(code, [lang]).value;
      },
      breaks: false,
    })
  });
  const getHtml = (md: string) => {
    const config = { ADD_TAGS: ['iframe'], KEEP_CONTENT: false };
    return DOMPurify.sanitize(marked(md),config);
  }
  return (
    <div dangerouslySetInnerHTML={{__html: getHtml(md)}}></div>
  );
}

