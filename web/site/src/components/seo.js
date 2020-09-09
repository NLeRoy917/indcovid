/**
 * SEO component that queries for data with
 *  Gatsby's useStaticQuery React hook
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from "react";
import PropTypes from "prop-types";
import Helmet from "react-helmet";
import { useStaticQuery, graphql } from "gatsby";
import og_image from '../images/landing-screenshot.png';

const siteUrl = 'https://indcovid.com'

function SEO({ description, lang, meta, title }) {
  const { site } = useStaticQuery(
    graphql`
      query {
        site {
          siteMetadata {
            title
            description
            author
          }
        }
      }
    `
  )

  const metaDescription = description || site.siteMetadata.description

  return (
    <Helmet
      htmlAttributes={{
        lang,
      }}
      title={title}
      titleTemplate={`${site.siteMetadata.title}`}
      meta={[
        {
          name: `description`,
          content: metaDescription,
        },
        {
          property: `og:type`,
          content: `website`,
        },
        {
          name: `twitter:card`,
          content: `summary`,
        },
        {
          name: `twitter:creator`,
          content: site.siteMetadata.author,
        },
        {
          name: `twitter:title`,
          content: title,
        },
        {
          name: `twitter:description`,
          content: metaDescription,
        },
      ].concat(meta)}
    >
    <meta
      name="description"
      content="On this site, we investigate how people from communities who historically face health disparities are disproportionately affected by the COVID-19 pandemic."
    />
      <meta name="author" content="Nathan LeRoy & Barnabas Obeng-Gyasi" />
      <meta prefix="og: http://ogp.me/ns#" property="og:title" content="Indiana COVID-19 & Health Equity" />
      <meta prefix="og: http://ogp.me/ns#" property='og:description' content="On this site, we investigate how people from communities who historically face health disparities are disproportionately affected by the COVID-19 pandemic." />
      <meta prefix="og: http://ogp.me/ns#" property="og:url" content="https://indcovid.com" />
      <meta prefix="og: http://ogp.me/ns#" property="og:image" content={`${siteUrl}${og_image}`} />
    </Helmet>

  )
}

SEO.defaultProps = {
  lang: `en`,
  meta: 'Indiana COVID-19 & Health Equity',
  description: ``,
}

SEO.propTypes = {
  description: PropTypes.string,
  lang: PropTypes.string,
  meta: PropTypes.arrayOf(PropTypes.object),
  title: PropTypes.string.isRequired,
}

export default SEO
