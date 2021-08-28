import React, { useEffect } from 'react';
import { convertToHtml } from '../utils/markdown-util';

type MarkdownProps = {
  md: string;
}

export const Markdown = ({ md }: MarkdownProps) => {
  return (
    <div>
      <div className='markdown-area' dangerouslySetInnerHTML={{ __html: convertToHtml(md) }}></div>
    </div>
  );
}

