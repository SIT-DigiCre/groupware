import Head from 'next/head'

type PageHeadProps = {
  title: string
  description: string
  img?: string
}

const PageHead = ({ title, description, img }:PageHeadProps) => {
  let text = description;
  if(description.length > 120){
    text = text.substring(0,120)+'...'
  }
  return (
    <Head>
      <meta name="description" content={title} />
      <meta property="og:type" content="website" />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={text} />
      {img ?
        <>
          <meta name="twitter:card" content="summary_large_image" />
          <meta property="og:image" content={img} />
        </> :
        <>
          <meta name="twitter:card" content="summary" />
        </>
      }
    </Head>
  )
}

export default PageHead
