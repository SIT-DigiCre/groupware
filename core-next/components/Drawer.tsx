import Link from "next/link";
import { useState } from "react";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Badge from "@material-ui/core/Badge";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import DescriptionIcon from "@material-ui/icons/Description";
import CreateIcon from "@material-ui/icons/Create";
import ChatIcon from "@material-ui/icons/Chat";
import SettingsIcon from "@material-ui/icons/Settings";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import GroupIcon from "@material-ui/icons/Group";
import AttachMoneyIcon from "@material-ui/icons/AttachMoney";
import NotificationsIcon from "@material-ui/icons/Notifications";

const MiniDrawer = (props) => {
  const [open, setOpen] = useState(false);
  const toggleDrawer =
    (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event.type === "keydown" &&
        ((event as React.KeyboardEvent).key === "Tab" ||
          (event as React.KeyboardEvent).key === "Shift")
      ) {
        return;
      }

      setOpen(open);
    };
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            onClick={() => {
              setOpen(true);
            }}
          >
            <MenuIcon style={{ color: "white" }} />
          </IconButton>
          <Typography variant="h6" style={{ marginLeft: "5px" }}>
            ﾃﾞｼﾞｺｱ2.0ﾌﾟﾛﾄﾀｲﾌﾟ
          </Typography>
          <div style={{ flexGrow: 1 }}></div>
          <IconButton color="inherit">
            <Badge badgeContent={17} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer anchor="left" open={open} onClose={toggleDrawer(false)}>
        <List>
          <ListItem button key="chat">
            <ListItemIcon>
              <ChatIcon />
            </ListItemIcon>
            <ListItemText primary="×Chat" />
          </ListItem>
          <ListItem button key="ringi">
            <ListItemIcon>
              <AttachMoneyIcon />
            </ListItemIcon>
            <ListItemText primary="×Ringi" />
          </ListItem>
          <Link href="/work">
            <ListItem button key="work">
              <ListItemIcon>
                <CreateIcon />
              </ListItemIcon>
              <ListItemText primary="Work" />
            </ListItem>
          </Link>
          <ListItem button key="member">
            <ListItemIcon>
              <GroupIcon />
            </ListItemIcon>
            <ListItemText primary="×Member" />
          </ListItem>
          <Link href="/blog">
            <ListItem button key="blog">
              <ListItemIcon>
                <DescriptionIcon />
              </ListItemIcon>
              <ListItemText primary="Blog" />
            </ListItem>
          </Link>
        </List>
        <Divider />
        <List>
          <ListItem button key="setting">
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="×Setting" />
          </ListItem>
          <ListItem button key="logout">
            <ListItemIcon>
              <ExitToAppIcon />
            </ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItem>
        </List>
      </Drawer>
      {props.children}
    </div>
  );
};

export default MiniDrawer;
