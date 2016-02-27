case ets:lookup(store_nodes, all) of 
    [{store_nodes,all,[]}] ->
	 io:format("yes: ~p~n",[]);
    [{store_nodes,all, Nodes}] ->
	 io:format("no: ~p~n",[Nodes])
end.

