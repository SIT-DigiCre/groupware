from .models import Channel


def get_user_channel(request):
    channel_list_tmp = []
    channel_name_list = ['general', 'random', '定例会', 'form']
    channel_name_list.append(str(request.user.profile.generation) + 'th')
    for division in request.user.profile.divisions.all():
        channel_name_list.append(division.name)
    for channel_name_tmp in channel_name_list:
        chan_tmp = Channel.objects.filter(name=channel_name_tmp).first()
        if chan_tmp is None:
            chan_tmp = Channel()
            chan_tmp.name = channel_name_tmp
            chan_tmp.save()
        channel_list_tmp.append(chan_tmp)
    return tuple(channel_list_tmp)
