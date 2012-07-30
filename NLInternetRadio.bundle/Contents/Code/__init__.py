MUSIC_PREFIX = "/music/nlinternetradio"
NAME = L('Title')
ART  = 'art-default.jpg'
ICON = 'icon-default.png'
NOSTREAM = 'icon-nostream.png'


####################################################################################################

def Start():

    ## make this plugin show up in the 'Music' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(MUSIC_PREFIX, MusicMainMenu, NAME, ICON, ART, NOSTREAM)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
    

    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "WallStream"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = 1

####################################################################################################
def MusicMainMenu():
    
    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="PanelStream")
    Log('opening NL Internet Radio xml')
    
    #  Add Categories
    page = XML.ElementFromURL("http://bit.ly/txlk5T")
    
    for item in page.getiterator('item'):
        streamUrl=item.findtext("url")
        ext=item.findtext("ext")
        title=item.findtext("title")
        descr="Luisteren naar: " + item.findtext("title")
        link = item.findtext("thumb")
        bg_art = item.findtext("art")
        
        #dir.Append(TrackItem(streamUrl,title,subtitle=None,ext=ext, thumb=Function(GetThumb, vl=link),ext=ext))
        dir.Append(Function(TrackItem(PlaySong,title,thumb=Function(GetThumb, vl=link)),ext=ext, songID=streamUrl))
    # ... and then return the container
    return dir
####################################################################################################
def GetThumb(vl):
	try:
		image = HTTP.Request(vl, cacheTime=CACHE_1MONTH).content
		return DataObject(image, 'image/jpeg')
	except:
		return Redirect(R(NOSTREAM))
####################################################################################################
def PlaySong(sender, songID):
	streamUrl = songID
	Log(streamUrl)
	return Redirect(streamUrl)