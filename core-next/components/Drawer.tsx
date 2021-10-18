import Link from "next/link";
import { useEffect, useState } from "react";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Badge from "@mui/material/Badge";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import DescriptionIcon from "@mui/icons-material/Description";
import CreateIcon from "@mui/icons-material/Create";
import ChatIcon from "@mui/icons-material/Chat";
import SettingsIcon from "@mui/icons-material/Settings";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import GroupIcon from "@mui/icons-material/Group";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import NotificationsIcon from "@mui/icons-material/Notifications";
import DesktopWindowsIcon from '@mui/icons-material/DesktopWindows';
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";
import { tokenSlice } from "../store/token";
import { userInfoSlice } from "../store/user";
import { useRouter } from "next/dist/client/router";
import { Avatar, Button } from "@mui/material";
import { UserInfo } from "../interfaces/account";

const MiniDrawer = (props) => {
  const router = useRouter();
  const dispatch = useDispatch();
  const userInfo = useSelector((state: RootState) => state.user.user);
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
  const movePage = (url: string) => 
    router.push(url).then(res=>setOpen(false));
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
          {userInfo !== null ? (
            <Avatar alt={userInfo.username} src={userInfo.icon} />
          ) : (
            <Button variant="contained" color="secondary" href="/login">
              ログイン
            </Button>
          )}
          {/*
          <IconButton color="inherit">
            <Badge badgeContent={17} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          */}
        </Toolbar>
      </AppBar>
      <Drawer anchor="left" open={open} onClose={toggleDrawer(false)}>
        <List>
        <div onClick={()=>{movePage('/')}}>
            <ListItem button key="top">
              <ListItemIcon>
                <DesktopWindowsIcon />
              </ListItemIcon>
              <ListItemText primary="Top" />
            </ListItem>
          </div>
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
          <div onClick={()=>{movePage('/work')}}>
            <ListItem button key="work">
              <ListItemIcon>
                <CreateIcon />
              </ListItemIcon>
              <ListItemText primary="Work" />
            </ListItem>
          </div>
          <ListItem button key="member">
            <ListItemIcon>
              <GroupIcon />
            </ListItemIcon>
            <ListItemText primary="×Member" />
          </ListItem>
          <div onClick={()=>{movePage('/blog')}}>
            <ListItem button key="blog">
              <ListItemIcon>
                <DescriptionIcon />
              </ListItemIcon>
              <ListItemText primary="Blog" />
            </ListItem>
          </div>
        </List>
        <Divider />
        <List>
          <ListItem button key="setting">
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="×Setting" />
          </ListItem>
          <ListItem
            button
            key="logout"
            onClick={() => {
              dispatch(userInfoSlice.actions.reset());
              dispatch(tokenSlice.actions.reset());
            }}
          >
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
