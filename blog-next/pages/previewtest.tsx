import { ReactEventHandler, useState } from 'react';
import { Container, Col, Row, Form } from 'react-bootstrap';
import { Markdown } from '../components/Markdown';

const PreviewTestPage = () => {
  const [md, setMd] = useState('');
  const handleOnChangeTextArea = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMd(e.target.value);
  }
  return (
    <Container>
      <Row className='mt-2'>
        <h1>デジコアブログMarkdownテストページ</h1>
        <p>デジコアブログで試用しているMarkdownビュワーの表示の確認に使用します。デジコア2.0実装までの応急対策としてこのページは存在します。</p>
      </Row>
      <Row className='mt-2'>
        <Col md={6}>
          <Form.Control
            as="textarea"
            placeholder="プレビューしたいMarkdownテキストをここに入力"
            rows={30}
            value={md}
            onChange={handleOnChangeTextArea}
          />
        </Col>
        <Col md={6}>
          <Markdown md={md}></Markdown>
        </Col>
      </Row>

    </Container>
  );
}

export default PreviewTestPage;