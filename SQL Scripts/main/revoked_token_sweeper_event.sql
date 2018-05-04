create event old_revoke_sweeper 
	on SCHEDULE EVERY 8 hour 
    comment 'Clean up expired tokens.' 
    do 
		delete from revoked_tokens 
		where time < DATE_SUB(Now(), Interval 8 hour);
