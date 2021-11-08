import { Typography, Link } from "@mui/material";
import MuiBreadcrumbs from "@mui/material/Breadcrumbs";

type LinkData = {
  name: string
  url?: string
}

type PropType = {
  links: LinkData[]
}

const Breadcrumbs = (props: PropType) => {
  return (
  <MuiBreadcrumbs>
    <Link underline="hover" color="inherit" href="/">
      Top
    </Link>
    {props.links.map(link => {
      if(link.url === undefined){
        return(
          <Typography color="GrayText.primary">{link.name}</Typography>
        );
      }else{
        return(
          <Link underline="hover" color="inherit" href={link.url}>
            {link.name}
          </Link>
        );
      }
    })}
  </MuiBreadcrumbs>
  );
}

export default Breadcrumbs;