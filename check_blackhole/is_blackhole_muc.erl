case ets:lookup(store_nodes, muc) of 
    [{store_nodes,muc,[]}] ->
	 io:format("yes: ~p~n",[]);
    [{store_nodes,muc, Nodes}] ->
	 io:format("no: ~p~n",[Nodes])
end.

